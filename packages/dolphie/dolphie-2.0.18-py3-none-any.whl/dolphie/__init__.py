import ipaddress
import os
import re
import socket
import sys
from datetime import datetime
from importlib import metadata
from time import sleep

import pymysql
import requests
from dolphie.Database import Database
from dolphie.Functions import format_bytes, format_number, format_sys_table_memory
from dolphie.KBHit import KBHit
from dolphie.ManualException import ManualException
from dolphie.Queries import Queries
from packaging.version import parse as parse_version
from rich import box
from rich.align import Align
from rich.console import Console
from rich.layout import Layout
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from sqlparse import format as sqlformat

try:
    __package_name__ = metadata.metadata(__package__ or __name__)["Name"]
    __version__ = metadata.version(__package__ or __name__)
except Exception:
    __package_name__ = "N/A"
    __version__ = "N/A"


class Dolphie:
    def __init__(self):
        self.console = Console()
        self.kb = KBHit()
        self.rich_live = None

        # Config options
        self.user: str = None
        self.password: str = None
        self.host: str = None
        self.port: int = 3306
        self.socket: str = None
        self.ssl: dict = {}
        self.config_file: str = None
        self.host_cache_file: str = None
        self.debug: bool = False
        self.refresh_interval: int = 1
        self.refresh_interval_innodb_status: int = 1
        self.dashboard: bool = True
        self.use_processlist: bool = False
        self.show_idle_queries: bool = False
        self.show_trxs_only: bool = False
        self.show_additional_query_columns: bool = False
        self.show_last_executed_query: bool = False
        self.sort_by_time_descending: bool = True
        self.heartbeat_table: str = None
        self.user_filter: str = None
        self.db_filter: str = None
        self.host_filter: str = None
        self.time_filter: str = 0
        self.query_filter: str = None

        # Loop variables
        self.dolphie_start_time: datetime = datetime.now()
        self.previous_main_loop_time: datetime = datetime.now()
        self.previous_innodb_status_loop_time: datetime = datetime.now()
        self.loop_duration_seconds: int = 0
        self.processlist_threads: dict = {}
        self.pause_refresh: bool = False
        self.first_loop: bool = True
        self.saved_status: bool = None
        self.previous_binlog_position: int = 0
        self.previous_replica_sbm: int = 0
        self.host_cache: dict = {}
        self.host_cache_from_file: dict = {}
        self.variables: dict = {}
        self.statuses: dict = {}
        self.primary_status: dict = {}
        self.replica_status: dict = {}
        self.innodb_status: dict = {}
        self.replica_connections: dict = {}

        # Set on database connection
        self.connection_id: int = None
        self.use_performance_schema: bool = False
        self.performance_schema_enabled: bool = False
        self.innodb_locks_sql: bool = False
        self.host_is_rds: bool = False
        self.server_uuid: str = None
        self.mysql_version: str = None
        self.host_distro: str = None

        self.app_version = __version__
        self.header_title = f"[b steel_blue1]dolphie[/b steel_blue1] :dolphin: v{self.app_version}"

    def check_for_update(self):
        # Query PyPI API to get the latest version
        url = f"https://pypi.org/pypi/{__package_name__}/json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # Extract the latest version from the response
            latest_version = data["info"]["version"]

            # Compare the current version with the latest version
            if parse_version(latest_version) > parse_version(__version__):
                self.console.print(
                    (
                        "[bright_green]New version available!\n\n[grey93]Current version:"
                        f" [steel_blue1]{__version__}\n[grey93]Latest version:"
                        f" [steel_blue1]{latest_version}\n\n[grey93]Please update to the latest version at your"
                        " convenience\n[grey66]You can find more details at:"
                        " [underline]https://github.com/charles-001/dolphie[/underline]\n\n[steel_blue1]Press any key"
                        " to continue"
                    ),
                    highlight=False,
                )

                key = self.kb.key_press_blocking()
                if key:
                    pass
        else:
            self.console.print(
                f"[indian_red]Failed to retrieve package information from PyPI![/indian_red] URL: {url} - Code:"
                f" {response.status_code}"
            )

    def update_environment_variables_for_pager(self):
        # Must do this so color is enabled for pager commands
        os.environ["PAGER"] = "less -R"
        os.environ["TERM"] = "xterm-256color"

    def create_rich_layout(self) -> Layout:
        layout = Layout(name="root")

        layout.split_column(
            Layout(name="header", size=1),
            Layout(name="dashboard", size=13),
            Layout(name="innodb_io", visible=False, size=10),
            Layout(name="replicas", visible=False),
            Layout(name="innodb_locks", visible=False),
            Layout(name="processlist"),
            Layout(name="footer", size=1, visible=False),
        )

        layout["dashboard"].update("")
        layout["processlist"].update("")
        layout["footer"].update("")

        self.layout = layout

    def update_footer(self, output):
        self.layout["footer"].visible = True

        self.layout["footer"].update(output)
        self.rich_live.update(self.layout, refresh=True)
        sleep(1.5)
        self.layout["footer"].update("")

        self.layout["footer"].visible = False

    def db_connect(self):
        self.db = Database(self.host, self.user, self.password, self.socket, self.port, self.ssl)

        query = "SELECT CONNECTION_ID() AS connection_id"
        self.connection_id = self.db.fetchone(query, "connection_id")

        query = "SELECT @@performance_schema"
        performance_schema = self.db.fetchone(query, "@@performance_schema")
        if performance_schema == 1:
            self.performance_schema_enabled = True

            if not self.use_processlist:
                self.use_performance_schema = True

        query = "SELECT @@version_comment"
        version_comment = self.db.fetchone(query, "@@version_comment").lower()

        query = "SELECT @@basedir"
        basedir = self.db.fetchone(query, "@@basedir")

        aurora_version = None
        query = "SHOW GLOBAL VARIABLES LIKE 'aurora_version'"
        aurora_version_data = self.db.fetchone(query, "Value")
        if aurora_version_data:
            aurora_version = aurora_version_data["Value"]

        query = "SELECT @@version"
        version = self.db.fetchone(query, "@@version").lower()
        version_split = version.split(".")

        self.mysql_version = "%s.%s.%s" % (
            version_split[0],
            version_split[1],
            version_split[2].split("-")[0],
        )
        major_version = int(version_split[0])

        # Get proper host version and fork
        if "percona xtradb cluster" in version_comment:
            self.host_distro = "Percona XtraDB Cluster"
        elif "percona server" in version_comment:
            self.host_distro = "Percona Server"
        elif "mariadb cluster" in version_comment:
            self.host_distro = "MariaDB Cluster"
        elif "mariadb" in version_comment or "mariadb" in version:
            self.host_distro = "MariaDB"
        elif aurora_version:
            self.host_distro = "Amazon Aurora"
            self.host_is_rds = True
        elif "rdsdb" in basedir:
            self.host_distro = "Amazon RDS"
            self.host_is_rds = True
        else:
            self.host_distro = "MySQL"

        # Determine if InnoDB locks panel is available for a version and which query to use
        self.innodb_locks_sql = None
        server_uuid_query = "SELECT @@server_uuid"
        if "MariaDB" in self.host_distro and major_version >= 10:
            server_uuid_query = "SELECT @@server_id AS @@server_uuid"
            self.innodb_locks_sql = Queries["locks_query-5"]
        elif major_version == 5:
            self.innodb_locks_sql = Queries["locks_query-5"]
        elif major_version == 8 and self.use_performance_schema:
            self.innodb_locks_sql = Queries["locks_query-8"]

        self.server_uuid = self.db.fetchone(server_uuid_query, "@@server_uuid")

        self.header_title = (
            f"{self.header_title} [b steel_blue1]\\[[/b steel_blue1][grey78]{self.host}[/grey78][b steel_blue1]][/b"
            " steel_blue1]"
        )
        self.layout["header"].update(Align.right(Text.from_markup(f"{self.header_title} [dim]press ? for help[/dim]")))

    def fetch_data(self, command):
        command_data = {}

        if command == "status" or command == "variables":
            self.db.execute(Queries[command])
            data = self.db.fetchall()

            for row in data:
                variable = row["Variable_name"]
                value = row["Value"]

                try:
                    converted_value = row["Value"]

                    if converted_value.isnumeric():
                        converted_value = int(converted_value)
                except (UnicodeDecodeError, AttributeError):
                    converted_value = value

                command_data[variable] = converted_value

        elif command == "innodb_status":
            data = self.db.fetchone(Queries[command], "Status")
            command_data["status"] = data

        else:
            self.db.execute(Queries[command])
            data = self.db.fetchall()

            for row in data:
                for column, value in row.items():
                    try:
                        converted_value = value

                        if converted_value.isnumeric():
                            converted_value = int(converted_value)
                    except (UnicodeDecodeError, AttributeError):
                        converted_value = value

                    command_data[column] = converted_value

        return command_data

    def block_refresh_for_key_command(self, refresh=False):
        if refresh:
            self.layout["footer"].visible = True
            self.layout["footer"].update(Align.center("[b]Paused![/b] Press any key to return", style="steel_blue1"))
            self.rich_live.update(self.layout, refresh=True)
        else:
            self.console.print(Align.center("\n[b]Paused![/b] Press any key to return", style="steel_blue1"))

        key = self.kb.key_press_blocking()
        if key:
            self.layout["footer"].update("")
            self.layout["footer"].visible = False
            return

    def capture_key(self, key):
        self.pause_refresh = True
        valid_key = True

        self.kb.set_normal_term()

        if key == "1":
            if self.use_performance_schema:
                self.use_performance_schema = False
                self.update_footer("[steel_blue1]Switched to [grey93]Processlist")
            else:
                if self.performance_schema_enabled:
                    self.use_performance_schema = True
                    self.update_footer("[steel_blue1]Switched to [grey93]Performance Schema")
                else:
                    self.update_footer("[indian_red]You can't switch to Performance Schema because it isn't enabled")

        elif key == "2":
            self.rich_live.stop()

            os.system("clear")

            table = Table(
                show_header=False,
                caption="Press q to return",
                box=box.SIMPLE,
            )
            table.add_column("")
            table.add_row(self.innodb_status["status"])

            with self.console.pager(styles=True):
                self.console.print(Align.right(f"{self.header_title} [dim]press q to return"), highlight=False)
                self.console.print(table)

            self.rich_live.start()

        elif key == "a":
            if self.show_additional_query_columns:
                self.show_additional_query_columns = False
            else:
                self.show_additional_query_columns = True

        elif key == "C":
            self.user_filter = ""
            self.db_filter = ""
            self.host_filter = ""
            self.time_filter = ""
            self.query_filter = ""

            self.update_footer("[steel_blue1]Cleared all filters!")

        elif key == "d":
            if self.layout["dashboard"].visible:
                self.layout["dashboard"].visible = False
            else:
                self.layout["dashboard"].visible = True

        elif key == "D":
            self.db_filter = self.console.input("[steel_blue1]Database to filter by[/steel_blue1]: ")

        elif key == "E":
            if not self.mysql_version.startswith("8"):
                self.update_footer("[indian_red]This command requires MySQL 8!")
            else:
                event_levels = {
                    "a": "all",
                    "s": "system",
                    "w": "warning",
                    "e": "error",
                }
                available_levels = ", ".join(
                    f"[b steel_blue1]{key}[/b steel_blue1]=[grey70]{value}[/grey70]"
                    for key, value in event_levels.items()
                )
                while True:
                    event_levels_input = self.console.input(
                        (
                            "[steel_blue1]What level(s) of events do you want to display? Use a comma to"
                            f" separate[/steel_blue1] \\[{available_levels}]: "
                        ),
                    )

                    # Split the input by commas and remove leading/trailing whitespaces
                    selected_levels = [level.strip() for level in event_levels_input.split(",")]

                    # Check if all selected levels are valid
                    if all(level in event_levels.keys() for level in selected_levels):
                        break
                    else:
                        self.update_footer("[indian_red]Invalid level")

                table = Table(
                    show_header=False,
                    caption="Press q to return",
                    box=box.SIMPLE,
                )
                table.add_column("Time", style="dim")
                table.add_column("Level")
                table.add_column("Event")

                query = Queries["error_log"]
                where_clauses = {
                    "s": 'prio = "System"',
                    "w": 'prio = "Warning"',
                    "e": 'prio = "Error"',
                }

                if "a" not in selected_levels:
                    where_conditions = [where_clauses[level] for level in selected_levels if level in where_clauses]
                    where_clause = " OR ".join(where_conditions)
                    query = query.replace("$placeholder", f"AND ({where_clause})")
                else:
                    query = query.replace("$placeholder", "")

                self.db.execute(query)
                data = self.db.fetchall()
                for row in data:
                    level_color = "grey93"
                    if row["level"] == "Error":
                        level_color = "white on red"
                    elif row["level"] == "Warning":
                        level_color = "bright_yellow"

                    level = f"[{level_color}]{row['level']}[/{level_color}]"
                    table.add_row(row["timestamp"].strftime("%Y-%m-%d %H:%M:%S"), level, row["message"])

                self.rich_live.stop()

                os.system("clear")
                with self.console.pager(styles=True):
                    self.console.print(Align.right(f"{self.header_title} [dim]press q to return"), highlight=False)
                    self.console.print(table)

                self.rich_live.start()

        elif key == "e":
            thread_id = self.console.input("[steel_blue1]Thread ID to explain[/steel_blue1]: ")

            if thread_id:
                if thread_id in self.processlist_threads:
                    os.system("clear")
                    self.console.print(Align.right(self.header_title), highlight=False)

                    row_style = Style(color="grey93")
                    table = Table(box=box.ROUNDED, show_header=False, style="grey70")
                    table.add_column("")
                    table.add_column("")

                    table.add_row("[gray78]Thread ID", str(thread_id), style=row_style)
                    table.add_row(
                        "[gray78]User",
                        self.processlist_threads[thread_id]["user"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Host",
                        self.processlist_threads[thread_id]["host"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Database",
                        self.processlist_threads[thread_id]["db"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Command",
                        self.processlist_threads[thread_id]["command"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]State",
                        self.processlist_threads[thread_id]["state"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Time",
                        self.processlist_threads[thread_id]["hhmmss_time"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Rows Locked",
                        self.processlist_threads[thread_id]["trx_rows_locked"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]Rows Modified",
                        self.processlist_threads[thread_id]["trx_rows_modified"],
                        style=row_style,
                    )
                    if "innodb_thread_concurrency" in self.variables and self.variables["innodb_thread_concurrency"]:
                        table.add_row(
                            "[gray78]Tickets",
                            self.processlist_threads[thread_id]["trx_concurrency_tickets"],
                            style=row_style,
                        )
                    table.add_row("", "")
                    table.add_row(
                        "[gray78]TRX State",
                        self.processlist_threads[thread_id]["trx_state"],
                        style=row_style,
                    )
                    table.add_row(
                        "[gray78]TRX Operation",
                        self.processlist_threads[thread_id]["trx_operation_state"],
                        style=row_style,
                    )

                    self.console.print(Align.center(table))

                    query = sqlformat(self.processlist_threads[thread_id]["query"], reindent_aligned=True)
                    query_db = self.processlist_threads[thread_id]["db"]

                    if query:
                        self.console.print("")

                        # This is just to make the theme is wrapped around only the query and not expanded out
                        # further than it needs to be
                        query_width = 0
                        for line in query.split("\n"):
                            if len(line) > query_width:
                                query_width = len(line)

                        if query_width >= self.console.width:
                            query_width = self.console.width - 2

                        self.console.print(
                            Align.center(
                                Syntax(
                                    query,
                                    "sql",
                                    line_numbers=False,
                                    word_wrap=True,
                                    theme="monokai",
                                    code_width=query_width,
                                    background_color="default",
                                )
                            )
                        )

                    if query and query_db:
                        explain_failure = None
                        explain_data = None

                        self.console.print("")
                        try:
                            self.db.cursor.execute("USE %s" % query_db)
                            self.db.cursor.execute("EXPLAIN %s" % query)

                            explain_data = self.db.fetchall()
                        except pymysql.Error as e:
                            explain_failure = "[b indian_red]EXPLAIN ERROR:[/b indian_red] [indian_red]%s" % e.args[1]

                        if explain_data:
                            explain_table = Table(box=box.ROUNDED, style="grey70")

                            columns = []
                            for row in explain_data:
                                values = []
                                for column, value in row.items():
                                    # Exclude possbile_keys field since it takes up too much space
                                    if column == "possible_keys":
                                        continue

                                    # Don't duplicate columns
                                    if column not in columns:
                                        explain_table.add_column(column)
                                        columns.append(column)

                                    if column == "key" and value is None:
                                        value = "[b white on red]NO INDEX[/b white on red]"

                                    if column == "rows":
                                        value = format_number(value)

                                    values.append(str(value))

                                explain_table.add_row(*values, style="grey93")

                            self.console.print(Align.center(explain_table))
                        else:
                            self.console.print(Align.center(explain_failure))

                    self.block_refresh_for_key_command()
                else:
                    self.update_footer("[indian_red]Thread ID '[grey93]%s[indian_red]' does not exist!" % thread_id)
            else:
                self.update_footer("[indian_red]There was no Thread ID specified!")

        elif key == "H":
            self.host_filter = self.console.input("[steel_blue1]Hostname/IP to filter by[/steel_blue1]: ")

            # Since our filtering is done by the processlist query, the value needs to be what's in host cache
            for ip, addr in self.host_cache.items():
                if self.host_filter == addr:
                    self.host_filter = ip

        elif key == "i":
            if self.layout["innodb_io"].visible:
                self.layout["innodb_io"].visible = False
            else:
                self.layout["innodb_io"].visible = True

        elif key == "I":
            if self.show_idle_queries:
                self.show_idle_queries = False
                self.sort_by_time_descending = True
            else:
                self.show_idle_queries = True
                self.sort_by_time_descending = False

        elif key == "k":
            thread_id = self.console.input("[steel_blue1]Thread ID to kill[/steel_blue1]: ")

            if thread_id:
                if thread_id in self.processlist_threads:
                    try:
                        if self.host_is_rds:
                            self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                        else:
                            self.db.cursor.execute("KILL %s" % thread_id)
                    except pymysql.OperationalError:
                        self.update_footer("[indian_red]Thread ID '[grey93]%s[indian_red]' does not exist!" % thread_id)
                else:
                    self.update_footer("[indian_red]Thread ID '[grey93]%s[indian_red]' does not exist!" % thread_id)

        elif key == "K":
            include_sleep = self.console.input("[steel_blue1]Include queries in sleep state? (y/n)[/steel_blue1]: ")

            if include_sleep != "y" and include_sleep != "n":
                self.update_footer("[indian_red]Invalid option!")
            else:
                kill_type = self.console.input(
                    "[steel_blue1]Kill by username/hostname/time range (u/h/t)[/steel_blue1]: "
                )
                threads_killed = 0

                commands_without_sleep = ["Query", "Execute"]
                commands_with_sleep = ["Query", "Execute", "Sleep"]

                if kill_type == "u":
                    user = self.console.input("[steel_blue1]User[/steel_blue1]: ")

                    for thread_id, thread in self.processlist_threads.items():
                        try:
                            if thread["user"] == user:
                                if include_sleep == "y":
                                    if thread["command"] in commands_with_sleep:
                                        if self.host_is_rds:
                                            self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                        else:
                                            self.db.cursor.execute("KILL %s" % thread_id)

                                        threads_killed += 1
                                else:
                                    if thread["command"] in commands_without_sleep:
                                        if self.host_is_rds:
                                            self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                        else:
                                            self.db.cursor.execute("KILL %s" % thread_id)

                                        threads_killed += 1
                        except pymysql.OperationalError:
                            continue

                elif kill_type == "h":
                    host = self.console.input("[steel_blue1]Host/IP[/steel_blue1]: ")

                    for thread_id, thread in self.processlist_threads.items():
                        try:
                            if thread["host"] == host:
                                if include_sleep == "y":
                                    if thread["command"] in commands_with_sleep:
                                        if self.host_is_rds:
                                            self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                        else:
                                            self.db.cursor.execute("KILL %s" % thread_id)

                                        threads_killed += 1
                                else:
                                    if thread["command"] in commands_without_sleep:
                                        if self.host_is_rds:
                                            self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                        else:
                                            self.db.cursor.execute("KILL %s" % thread_id)

                                        threads_killed += 1
                        except pymysql.OperationalError:
                            continue

                elif kill_type == "t":
                    time = self.console.input("[steel_blue1]Time range (ex. 10-20)[/steel_blue1]: ")

                    if re.search(r"(\d+-\d+)", time):
                        time_range = time.split("-")
                        lower_limit = int(time_range[0])
                        upper_limit = int(time_range[1])

                        if lower_limit > upper_limit:
                            self.update_footer(
                                "[indian_red]Invalid time range! Lower limit can't be higher than upper!"
                            )
                        else:
                            for thread_id, thread in self.processlist_threads.items():
                                try:
                                    if thread["time"] >= lower_limit and thread["time"] <= upper_limit:
                                        if include_sleep == "y":
                                            if thread["command"] in commands_with_sleep:
                                                if self.host_is_rds:
                                                    self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                                else:
                                                    self.db.cursor.execute("KILL %s" % thread_id)

                                                threads_killed += 1
                                        else:
                                            if thread["command"] in commands_without_sleep:
                                                if self.host_is_rds:
                                                    self.db.cursor.execute("CALL mysql.rds_kill(%s)" % thread_id)
                                                else:
                                                    self.db.cursor.execute("KILL %s" % thread_id)

                                                threads_killed += 1
                                except pymysql.OperationalError:
                                    continue
                    else:
                        self.update_footer("[indian_red]Invalid time range!")
                else:
                    self.update_footer("[indian_red]Invalid option!")

                if threads_killed:
                    self.update_footer("[grey93]Killed [steel_blue1]%s [grey93]threads!" % threads_killed)
                else:
                    self.update_footer("[indian_red]No threads were killed!")

        elif key == "l":
            if self.innodb_locks_sql:
                if self.layout["innodb_locks"].visible:
                    self.layout["innodb_locks"].visible = False
                else:
                    self.layout["innodb_locks"].visible = True
            else:
                self.update_footer("[indian_red]InnoDB Locks panel isn't supported for this host's version!")

        elif key == "L":
            os.system("clear")
            self.console.print(Align.right(self.header_title), highlight=False)

            deadlock = ""
            output = re.search(
                r"------------------------\nLATEST\sDETECTED\sDEADLOCK\n------------------------"
                "\n(.*?)------------\nTRANSACTIONS",
                self.innodb_status["status"],
                flags=re.S,
            )
            if output:
                deadlock = output.group(1)

                deadlock = deadlock.replace("***", "[yellow]*****[/yellow]")
                self.console.print(deadlock, highlight=False)
            else:
                self.console.print("No deadlock detected!", justify="center")

            self.block_refresh_for_key_command()

        elif key == "m":
            os.system("clear")
            self.console.print(Align.right(self.header_title), highlight=False)

            table_grid = Table.grid()

            table1 = Table(
                box=box.ROUNDED,
                style="grey70",
            )

            header_style = Style(bold=True)
            table1.add_column("User", header_style=header_style)
            table1.add_column("Current", header_style=header_style)
            table1.add_column("Total", header_style=header_style)

            self.db.execute(Queries["memory_by_user"])
            data = self.db.fetchall()
            for row in data:
                table1.add_row(
                    row["user"],
                    format_sys_table_memory(row["current_allocated"]),
                    format_sys_table_memory(row["total_allocated"]),
                )

            table2 = Table(
                box=box.ROUNDED,
                style="grey70",
            )
            table2.add_column("Code Area", header_style=header_style)
            table2.add_column("Current", header_style=header_style)

            self.db.execute(Queries["memory_by_code_area"])
            data = self.db.fetchall()
            for row in data:
                table2.add_row(row["code_area"], format_sys_table_memory(row["current_allocated"]))

            table3 = Table(
                box=box.ROUNDED,
                style="grey70",
            )
            table3.add_column("Host", header_style=header_style)
            table3.add_column("Current", header_style=header_style)
            table3.add_column("Total", header_style=header_style)

            self.db.execute(Queries["memory_by_host"])
            data = self.db.fetchall()
            for row in data:
                table3.add_row(
                    self.get_hostname(row["host"]),
                    format_sys_table_memory(row["current_allocated"]),
                    format_sys_table_memory(row["total_allocated"]),
                )

            table_grid.add_row("", Align.center("[b]Memory Allocation[/b]"), "")
            table_grid.add_row(table1, table3, table2)

            self.console.print(Align.center(table_grid))

            self.block_refresh_for_key_command()

        elif key == "p":
            if self.layout["processlist"].visible:
                self.layout["processlist"].visible = False
            else:
                self.layout["processlist"].visible = True

        elif key == "P":
            self.block_refresh_for_key_command(
                refresh=True,
            )

        elif key == "Q":
            self.query_filter = self.console.input("[steel_blue1]Query text to filter by[/steel_blue1]: ")

        elif key == "q":
            sys.exit()

        elif key == "r":
            if self.layout["replicas"].visible:
                self.layout["replicas"].visible = False

                # Cleanup connections
                for connection in self.replica_connections.values():
                    connection["connection"].close()

                self.replica_connections = {}
            else:
                self.layout["replicas"].visible = True

        elif key == "s":
            if self.sort_by_time_descending:
                self.sort_by_time_descending = False
            else:
                self.sort_by_time_descending = True

        elif key == "S":
            if self.show_last_executed_query:
                self.show_last_executed_query = False
            else:
                self.show_last_executed_query = True

        elif key == "t":
            if self.show_trxs_only:
                self.show_trxs_only = False
            else:
                self.show_trxs_only = True

        elif key == "T":
            time = self.console.input("[steel_blue1]Minimum time to display for queries[/steel_blue1]: ")

            if time.isnumeric():
                self.time_filter = int(time)
            else:
                self.update_footer("[indian_red]Time must be an integer!")

        elif key == "u":
            user_stat_data = self.create_user_stats_table()
            if user_stat_data:
                os.system("clear")
                self.console.print(Align.right(self.header_title), highlight=False)
                self.console.print(Align.center(user_stat_data))

                self.block_refresh_for_key_command()
            else:
                self.update_footer(
                    "[indian_red]This command requires Userstat variable or Performance Schema to be enabled!"
                )

        elif key == "U":
            self.user_filter = self.console.input("[steel_blue1]User to filter by[/steel_blue1]: ")

        elif key == "y":
            os.system("clear")
            self.console.print(Align.right(self.header_title), highlight=False)

            tables = {}
            all_tables = []

            db_count = self.db.execute(Queries["databases"])
            databases = self.db.fetchall()

            # Determine how many tables to provide data
            max_num_tables = 1 if db_count <= 20 else 3

            # Calculate how many databases per table
            row_per_count = db_count // max_num_tables

            # Create dictionary of tables
            for table_counter in range(1, max_num_tables + 1):
                tables[table_counter] = Table(box=box.ROUNDED, show_header=False, style="grey70")
                tables[table_counter].add_column("")

            # Loop over databases
            db_counter = 1
            table_counter = 1

            # Sort the databases by name
            for database in databases:
                tables[table_counter].add_row(database["SCHEMA_NAME"], style="grey93")
                db_counter += 1

                if db_counter > row_per_count and table_counter < max_num_tables:
                    table_counter += 1
                    db_counter = 1

            # Collect table data into an array
            all_tables = [table_data for table_data in tables.values() if table_data]

            table_grid = Table.grid()
            table_grid.add_row(*all_tables)

            self.console.print(Align.center("Databases"), style="b")
            self.console.print(Align.center(table_grid))
            self.console.print(Align.center("Total: [b steel_blue1]%s[/b steel_blue1]" % db_count))

            self.block_refresh_for_key_command()

        elif key == "v":
            input_variable = self.console.input(
                "[steel_blue1]Variable wildcard search ([grey78]leave blank for all[steel_blue1])[/steel_blue1]: "
            )

            os.system("clear")
            self.console.print(Align.right(self.header_title), highlight=False)

            size_convert_variables = [
                "audit_log_buffer_size",
                "audit_log_rotate_on_size",
                "binlog_cache_size",
                "binlog_row_event_max_size",
                "binlog_stmt_cache_size",
                "bulk_insert_buffer_size",
                "clone_buffer_size",
                "delay_queue_size",
                "histogram_generation_max_mem_size",
                "innodb_buffer_pool_chunk_size",
                "innodb_buffer_pool_size",
                "innodb_change_buffer_max_size",
                "innodb_ft_cache_size",
                "innodb_ft_total_cache_size",
                "innodb_log_buffer_size",
                "innodb_log_file_size",
                "innodb_log_write_ahead_size",
                "innodb_max_bitmap_file_size",
                "innodb_max_undo_log_size",
                "innodb_online_alter_log_max_size",
                "innodb_page_size",
                "innodb_sort_buffer_size",
                "join_buffer_size",
                "key_buffer_size",
                "key_cache_block_size",
                "large_page_size",
                "max_binlog_cache_size",
                "max_binlog_size",
                "max_binlog_stmt_cache_size",
                "max_heap_table_size",
                "max_join_size",
                "max_relay_log_size",
                "myisam_data_pointer_size",
                "myisam_max_sort_file_size",
                "myisam_mmap_size",
                "myisam_sort_buffer_size",
                "optimizer_trace_max_mem_size",
                "parser_max_mem_size",
                "preload_buffer_size",
                "query_alloc_block_size",
                "query_prealloc_size",
                "range_alloc_block_size",
                "range_optimizer_max_mem_size",
                "read_buffer_size",
                "read_rnd_buffer_size",
                "rpl_read_size",
                "slave_pending_jobs_size_max",
                "sort_buffer_size",
                "tmp_table_size",
                "transaction_alloc_block_size",
                "transaction_prealloc_size",
                "max_allowed_packet",
                "innodb_redo_log_capacity",
                "replica_max_allowed_packet",
                "mysqlx_max_allowed_packet",
                "global_connection_memory_limit",
                "temptable_max_mmap",
                "temptable_max_ram",
            ]

            table_grid = Table.grid()
            table_counter = 1
            variable_counter = 1
            row_counter = 1
            variable_num = 1
            all_tables = []
            tables = {}
            display_variables = {}

            for variable, value in self.variables.items():
                if input_variable:
                    if input_variable not in variable:
                        continue

                # Convert size variables so they're readable
                if variable in size_convert_variables:
                    try:
                        display_variables[variable] = format_bytes(self.variables[variable])
                    except KeyError:
                        display_variables[variable] = "N/A"
                else:
                    display_variables[variable] = value

            max_num_tables = 1 if len(display_variables) <= 20 else 3

            # Create the number of tables we want
            while table_counter <= max_num_tables:
                tables[table_counter] = Table(box=box.ROUNDED, show_header=False, style="grey70")
                tables[table_counter].add_column("")
                tables[table_counter].add_column("")

                table_counter += 1

            # Calculate how many variables per table
            row_per_count = len(display_variables) // max_num_tables

            # Loop variables
            for variable, value in display_variables.items():
                tables[variable_num].add_row("[gray78]%s" % variable, str(value), style="grey93")

                if variable_counter == row_per_count and row_counter != max_num_tables:
                    row_counter += 1
                    variable_counter = 0
                    variable_num += 1

                variable_counter += 1

            # Put all the variable data from dict into an array
            all_tables = [table_data for table_data in tables.values() if table_data]

            # Add the data into a single tuple for add_row
            if display_variables:
                table_grid.add_row(*all_tables)
                self.console.print(Align.center(table_grid))
                self.block_refresh_for_key_command()
            else:
                if input_variable:
                    self.update_footer("[indian_red]No variable(s) found that match your search!")

        elif key == "x":
            refresh_interval = self.console.input("[steel_blue1]Refresh interval (in seconds)[/steel_blue1]: ")

            if refresh_interval.isnumeric():
                self.refresh_interval = int(refresh_interval)
            else:
                self.update_footer("[indian_red]Input must be an integer!")

        elif key == "X":
            refresh_interval_innodb_status = self.console.input(
                "[steel_blue1]Refresh interval for InnoDB Status data (in seconds)[/steel_blue1]: "
            )

            if refresh_interval_innodb_status.isnumeric():
                self.refresh_interval_innodb_status = int(refresh_interval_innodb_status)
            else:
                self.update_footer("[indian_red]Input must be an integer!")

        elif key == "z":
            os.system("clear")
            self.console.print(Align.right(self.header_title), highlight=False)

            if self.host_cache:
                table = Table(box=box.ROUNDED, style="grey70")
                table.add_column("Host/IP")
                table.add_column("Hostname (if resolved)")

                for ip, addr in self.host_cache.items():
                    if ip:
                        table.add_row(ip, addr)

                self.console.print(Align.center("Host Cache"), style="b")
                self.console.print(Align.center(table))
                self.console.print(Align.center("Total: [b steel_blue1]%s" % len(self.host_cache)))
            else:
                self.console.print(Align.center("\nThere are currently no hosts resolved"))

            self.block_refresh_for_key_command()

        elif key == "?":
            self.rich_live.stop()

            os.system("clear")

            row_style = Style(color="grey93")

            filters = {
                "C": "Clear all filters",
                "D": "Filter by database",
                "H": "Filter by host/IP",
                "Q": "Filter by query text",
                "T": "Filter by minimum query time",
                "U": "Filter by user",
            }
            table_filters = Table(box=box.ROUNDED, style="grey70", title="Filters", title_style="bold steel_blue1")
            table_filters.add_column("Key", justify="center", style="b steel_blue1")
            table_filters.add_column("Description")
            for key, description in sorted(filters.items()):
                table_filters.add_row("[steel_blue1]%s" % key, description, style=row_style)

            panels = {
                "d": "Show/hide dashboard",
                "i": "Show/hide InnoDB information",
                "l": "Show/hide InnoDB query locks",
                "p": "Show/hide processlist",
                "r": "Show/hide replication",
            }
            table_panels = Table(box=box.ROUNDED, style="grey70", title="Panels", title_style="bold steel_blue1")
            table_panels.add_column("Key", justify="center", style="b steel_blue1")
            table_panels.add_column("Description")
            for key, description in sorted(panels.items()):
                table_panels.add_row("[steel_blue1]%s" % key, description, style=row_style)

            keys = {
                "1": "Switch between using Processlist/Performance Schema for listing queries",
                "2": "Display output from SHOW ENGINE INNODB STATUS using a pager",
                "a": "Show/hide additional processlist columns",
                "e": "Explain query of a thread and display thread information",
                "E": "Display error log from performance schema using a pager (MySQL 8 only)",
                "I": "Show/hide idle queries",
                "k": "Kill a query by thread ID",
                "K": "Kill a query by either user/host/time range",
                "L": "Show latest deadlock detected",
                "m": "Display memory usage - limits to only 30 rows",
                "P": "Pause Dolphie",
                "q": "Quit Dolphie",
                "t": "Show/hide running transactions only",
                "s": "Sort query list by time in descending/ascending order",
                "S": "Show/hide last executed query for sleeping thread (Performance Schema only)",
                "u": "List users (results vary depending on if userstat variable is enabled)",
                "v": "Variable wildcard search via SHOW VARIABLES",
                "x": "Set the general refresh interval",
                "X": "Set the refresh interval for data the query SHOW ENGINE INNODB STATUS is responsible for",
                "y": "Display all databases on host",
                "z": "Show all entries in the host cache",
            }

            table_keys = Table(box=box.ROUNDED, style="grey70", title="Features", title_style="bold steel_blue1")
            table_keys.add_column("Key", justify="center", style="b steel_blue1")
            table_keys.add_column("Description")

            for key, description in sorted(keys.items()):
                table_keys.add_row("[steel_blue1]%s" % key, description, style=row_style)

            datapoints = {
                "Read Only": "If the host is in read-only mode",
                "Use PS": "If Dolphie is using Performance Schema for listing queries",
                "Read Hit": "The percentage of how many reads are from InnoDB buffer pool compared to from disk",
                "Lag": (
                    "Retrieves metric from: Slave -> SHOW SLAVE STATUS, HB -> Heartbeat table, PS -> Performance Schema"
                ),
                "Chkpt Age": (
                    "This depicts how close InnoDB is before it starts to furiously flush dirty data to disk "
                    "(Higher is better)"
                ),
                "AHI Hit": (
                    "The percentage of how many lookups there are from Adapative Hash Index compared to it not"
                    " being used"
                ),
                "Pending AIO": "W means writes, R means reads. The values should normally be 0",
                "Diff": "This is the size difference of the binary log between each refresh interval",
                "Cache Hit": "The percentage of how many binary log lookups are from cache instead of from disk",
                "History List": "History list length (number of un-purged row changes in InnoDB's undo logs)",
                "Unpurged TRX": (
                    "How many transactions are between the newest and the last purged in InnoDB's undo logs"
                ),
                "QPS": "Queries per second",
                "Latency": "How much time it takes to receive data from the host for Dolphie each refresh interval",
                "Threads": "Con = Connected, Run = Running, Cac = Cached from SHOW GLOBAL STATUS",
                "Speed": "How many seconds were taken off of replication lag from the last refresh interval",
                "Query A/Q": (
                    "How many queries are active/queued in InnoDB. Based on innodb_thread_concurrency variable"
                ),
                "Tickets": "Relates to innodb_concurrency_tickets variable",
            }

            table_info = Table(box=box.ROUNDED, style="grey70")
            table_info.add_column("Datapoint", style="steel_blue1")
            table_info.add_column("Description")
            for datapoint, description in sorted(datapoints.items()):
                table_info.add_row("[steel_blue1]%s" % datapoint, description, style=row_style)

            table_grid = Table.grid()
            table_grid.add_row(table_panels, table_filters)

            with self.console.pager(styles=True):
                self.console.print(
                    Align.right(self.header_title + " [dim]press q to return\n"),
                    highlight=False,
                )
                self.console.print(Align.center(table_keys))
                self.console.print("")
                self.console.print(Align.center(table_grid))
                self.console.print("")
                self.console.print(Align.center(table_info))
                self.console.print("")
                self.console.print(Align.center("[dim]Press q to return"))
            self.rich_live.start()
        else:
            valid_key = False

        self.pause_refresh = False
        self.kb.set_new_term()

        return valid_key

    def create_user_stats_table(self):
        table = Table(header_style="bold white", box=box.ROUNDED, style="grey70")

        columns = {}
        user_stats = {}
        userstat_enabled = 0

        if self.db.execute("SELECT @@userstat", ignore_error=True) == 1:
            userstat_enabled = self.db.cursor.fetchone()["@@userstat"]

        if userstat_enabled:
            self.db.execute(Queries["userstat_user_statisitics"])

            columns.update(
                {
                    "User": {"field": "user", "format_number": False},
                    "Active": {"field": "concurrent_connections", "format_number": True},
                    "Total": {"field": "total_connections", "format_number": True},
                    "Binlog Data": {"field": "binlog_bytes_written", "format_number": False},
                    "Rows Read": {"field": "table_rows_read", "format_number": True},
                    "Rows Sent": {"field": "rows_fetched", "format_number": True},
                    "Rows Updated": {"field": "rows_updated", "format_number": True},
                    "Selects": {"field": "select_commands", "format_number": True},
                    "Updates": {"field": "update_commands", "format_number": True},
                    "Other": {"field": "other_commands", "format_number": True},
                    "Commit": {"field": "commit_transactions", "format_number": True},
                    "Rollback": {"field": "rollback_transactions", "format_number": True},
                    "Access Denied": {"field": "access_denied", "format_number": True},
                    "Conn Denied": {"field": "denied_connections", "format_number": True},
                }
            )

        elif self.performance_schema_enabled:
            self.db.execute(Queries["ps_user_statisitics"])

            columns.update(
                {
                    "User": {"field": "user", "format_number": False},
                    "Active": {"field": "current_connections", "format_number": True},
                    "Total": {"field": "total_connections", "format_number": True},
                    "Rows Read": {"field": "rows_read", "format_number": True},
                    "Rows Sent": {"field": "rows_sent", "format_number": True},
                    "Rows Updated": {"field": "rows_affected", "format_number": True},
                    "Tmp Tables": {"field": "created_tmp_tables", "format_number": True},
                    "Tmp Disk Tables": {"field": "created_tmp_disk_tables", "format_number": True},
                }
            )
        else:
            return False

        users = self.db.fetchall()
        for user in users:
            username = user["user"]
            if userstat_enabled:
                user_stats.setdefault(username, {}).update(
                    user=username,
                    total_connections=user["total_connections"],
                    concurrent_connections=user.get("concurrent_connections"),
                    denied_connections=user.get("denied_connections"),
                    binlog_bytes_written=user.get("binlog_bytes_written"),
                    rows_fetched=user.get("rows_fetched"),
                    rows_updated=user.get("rows_updated"),
                    table_rows_read=user.get("table_rows_read"),
                    select_commands=user.get("select_commands"),
                    update_commands=user.get("update_commands"),
                    other_commands=user.get("other_commands"),
                    commit_transactions=user.get("commit_transactions"),
                    rollback_transactions=user.get("rollback_transactions"),
                    access_denied=user.get("access_denied"),
                    current_connections=user.get("current_connections"),
                    rows_affected=user.get("sum_rows_affected"),
                    rows_sent=user.get("sum_rows_sent"),
                    rows_read=user.get("sum_rows_examined"),
                    created_tmp_disk_tables=user.get("sum_created_tmp_disk_tables"),
                    created_tmp_tables=user.get("sum_created_tmp_tables"),
                )
            else:
                if username not in user_stats:
                    user_stats[username] = {
                        "user": username,
                        "total_connections": user["total_connections"],
                        "current_connections": user["current_connections"],
                        "rows_affected": user["sum_rows_affected"],
                        "rows_sent": user["sum_rows_sent"],
                        "rows_read": user["sum_rows_examined"],
                        "created_tmp_disk_tables": user["sum_created_tmp_disk_tables"],
                        "created_tmp_tables": user["sum_created_tmp_tables"],
                    }
                else:
                    # I would use SUM() in the query instead of this, but pymysql doesn't play well with it since I
                    # use use_unicode = 0 in the connection
                    user_stats[username]["rows_affected"] += user["sum_rows_affected"]
                    user_stats[username]["rows_sent"] += user["sum_rows_sent"]
                    user_stats[username]["rows_read"] += user["sum_rows_examined"]
                    user_stats[username]["created_tmp_disk_tables"] += user["sum_created_tmp_disk_tables"]
                    user_stats[username]["created_tmp_tables"] += user["sum_created_tmp_tables"]

        for column, data in columns.items():
            table.add_column(column, no_wrap=True)

        for user_data in user_stats.values():
            row_values = []
            for column, data in columns.items():
                value = user_data.get(data["field"])
                if column == "Binlog Data":
                    row_values.append(format_bytes(value) if value else "")
                elif data["format_number"]:
                    row_values.append(format_number(value) if value else "")
                else:
                    row_values.append(value or "")

            table.add_row(*row_values, style="grey93")

        return table if user_stats else False

    def load_host_cache_file(self):
        if os.path.exists(self.host_cache_file):
            with open(self.host_cache_file) as file:
                for line in file:
                    line = line.strip()
                    error_message = f"Host cache entry '{line}' is not properly formatted! Format: ip=hostname"

                    if "=" not in line:
                        raise ManualException(error_message)

                    host, hostname = line.split("=", maxsplit=1)
                    host = host.strip()
                    hostname = hostname.strip()

                    if not host or not hostname:
                        raise ManualException(error_message)

                    self.host_cache_from_file[host] = hostname

    def get_hostname(self, host):
        if host in self.host_cache:
            return self.host_cache[host]

        if self.host_cache_from_file and host in self.host_cache_from_file:
            self.host_cache[host] = self.host_cache_from_file[host]
            return self.host_cache_from_file[host]

        try:
            ipaddress.IPv4Network(host)
            hostname = socket.gethostbyaddr(host)[0]
            self.host_cache[host] = hostname
        except (ValueError, socket.error):
            self.host_cache[host] = host
            hostname = host

        return hostname
