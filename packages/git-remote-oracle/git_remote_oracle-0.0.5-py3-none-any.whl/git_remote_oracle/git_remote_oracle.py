# documentation links:
#  https://git-scm.com/docs/gitremote-helpers
#  https://git-scm.com/docs/git-fast-import

import time
import oracledb
import pexpect
import os
import sys
from configparser import ConfigParser
from datetime import datetime

DEBUG = ("1" == os.getenv("GR_ORACLE_DEBUG"))
DEBUG_GIT_OUTPUT = ("1" == os.getenv("GR_ORACLE_DEBUG_GIT"))
CONNECT_AS_SYSDBA = ("1" == os.getenv("GR_ORACLE_SYSDBA"))
DATETIME_FORMAT = "%d.%m.%Y %H:%M:%S"
PROGRESS = True
BATCH_SIZE = 20 if (os.getenv("GR_ORACLE_BATCHSIZE") is None) else int(os.getenv("GR_ORACLE_BATCHSIZE"))
OBJECT_TYPES = ['PACKAGE',
                'PACKAGE BODY',
                'TRIGGER',
                'VIEW',
                'TABLE',
                'PROCEDURE',
                'FUNCTION',
                'INDEX',
                'TYPE',
                'TYPE BODY',
                'SYNONYM',
                'JOB',
                'JAVA SOURCE',
                'JAVA RESOURCE']
GIT_DIR = os.getenv("GIT_DIR")

def print_fl(*args, **kwargs):
  print(*args, **kwargs, flush=True)
  if DEBUG_GIT_OUTPUT and ('file' not in kwargs):
    if len(args) > 1:
      args2 = [f"> {args[0]}", *args[1]]
    else:
      args2 = [f"> {args[0]}"]
    print_to_err(*args2, **kwargs)

def print_to_err(*args, **kwargs):
    print_fl(*args, **kwargs, file=sys.stderr)

def dbgw(s):
  global DEBUG
  if DEBUG:
    print_to_err(s, end='')

def dbg(s):
  global DEBUG
  if DEBUG:
    print_to_err(s)

def read_from_tty():
  with open("/dev/tty") as tty:
    res = tty.readline()
    dbg(f"tty: {res}")
    return res

def git_credential_fill(protocol, host):
  child = pexpect.spawn("git credential fill")
  child.sendline(f"protocol={protocol}")
  child.readline()
  child.sendline(f"host={host}")
  child.readline()
  child.sendline("")
  child.readline()
  prop = None
  try:
    child.expect("Username for .*")
    print_to_err("Username:")
    child.sendline(read_from_tty())
    child.readline()
    child.expect("Password for .*")
    print_to_err("Password:")
    child.sendline(read_from_tty())
    child.readline()
  except Exception as e:
    dbg(f"expected 'Username for' {e}")
    prop = child.before.decode()
  if prop is None:
    child.wait()
    prop = child.read().decode()
  dbg(f"prop: -->{prop}<--")
  config = ConfigParser()
  config.read_string('[config]\n' + prop)
  dbg(f"config: {config}")
  return config

def git_credential_approve(protocol, host, username, password):
  child = pexpect.spawn("git credential approve")
  child.sendline(f"protocol={protocol}")
  child.sendline(f"host={host}")
  child.sendline(f"username={username}")
  child.sendline(f"password={password}")
  child.sendline("")
  child.wait()

def git_credential_reject(protocol, host, username, password):
  child = pexpect.spawn("git credential reject")
  child.sendline(f"protocol={protocol}")
  child.sendline(f"host={host}")
  child.sendline(f"username={username}")
  child.sendline(f"password={password}")
  child.sendline("")
  child.wait()

def commit_block(curr_time, formatted_datetime, last_ddl):
  print_fl("commit refs/heads/main")
  print_fl(f"committer <notexisting@notexisting.com> {curr_time} +0000")
  if last_ddl is None:
    msg = f"> {formatted_datetime}"
  else:
    msg = f"> {formatted_datetime}, <= {last_ddl}"
  print_fl(f"data {len(msg)}")
  print_fl(msg)
  child = pexpect.spawn("git rev-parse HEAD")
  id = child.readline()
  id = id.decode().strip()
  dbg(f"id: {id}")
  if((not id.startswith("fatal:")) and (len(id)>10) and ("{id}" != "")):
    print_fl(f"from {id}")

def print_file_list(file_list):
  for fl in file_list:
    print_fl(f"M 100644 :{fl['id']} {fl['name']}")

def print_deleted_file_list(file_list):
  for fl in file_list:
    print_fl(f"D {fl['name']}")

def find_existing_objects():
  global GIT_DIR
  result = []
  real_names = []
  workspace = os.path.abspath(f"{GIT_DIR}/..")
  for object_type in OBJECT_TYPES:
    if os.path.isdir(f"{workspace}/{object_type}"):
      for file in os.listdir(f"{workspace}/{object_type}"):
        name = file.replace(".sql","")
        result.append((object_type.lower(), name.lower()))
        real_names.append((object_type, name))
  return result, real_names

def get_deleted_file_list(cursor, schema):
  global OBJECT_TYPES
  obj_types = ",".join([f"'{t}'" for t in OBJECT_TYPES])
  existing_objects, real_names = find_existing_objects()
  if len(existing_objects) > 0:
    result = []
    qry = """
      SELECT 
        object_type, object_name
      FROM all_objects
      WHERE
        lower(owner) = lower(:1)
        AND object_type IN (""" + obj_types + """)
        AND sharing <> 'METADATA LINK'
        AND generated = 'N'
        AND temporary = 'N'
        AND oracle_maintained = 'N'
      """
    dbg(f"qry: {qry}")
    res = cursor.execute(qry, [schema])
    db_objects = []
    for r in res.fetchall():
      db_objects.append((r[0].lower(), r[1].lower()))
    i = 0
    for r in existing_objects:
      if r not in db_objects:
        r = real_names[i]
        result.append({"name": f"{r[0]}/{r[1]}.sql"})
      i += 1
    return result
  else:
    return []

def build_query(columns):
  global OBJECT_TYPES

  obj_types = ",".join([f"'{t}'" for t in OBJECT_TYPES])

  return """
    SELECT 
      """ + columns + """
    FROM all_objects
    WHERE 
      lower(owner) = lower(:1)
      AND object_type IN (""" + obj_types + """)
      AND sharing <> 'METADATA LINK'
      AND last_ddl_time > :3
      AND generated = 'N'
      AND temporary = 'N'
      AND oracle_maintained = 'N'
    ORDER BY object_id
    """

def create_file_list(cursor, schema, last_ddl_time):
  global PROGRESS
  qry_columns = """
      object_id,
      object_name,
      owner,
      object_type,
      DBMS_METADATA.GET_DDL(REPLACE(DECODE(
							object_type,
							'PACKAGE','PACKAGE SPEC',
							'TYPE','TYPE SPEC',
							'JOB','PROCOBJ',
							object_type 
						),' ','_'), object_name, UPPER(:2)) AS DDL
  """
  qry_cnt = build_query("COUNT(*) AS cnt,:2 AS ignore")
  dbg(f"qry_cnt: {qry_cnt}")
  res = cursor.execute(qry_cnt, [schema, schema, last_ddl_time])
  if PROGRESS:
    print_fl(f"progress 2/?")
  
  qry = build_query(qry_columns)
  dbg(f"qry: {qry}")
  total = res.fetchone()[0]

  file_list = []
  for i in range(0,total-1,BATCH_SIZE):
    qry_offset = f"""
    OFFSET {i} ROWS FETCH NEXT {BATCH_SIZE} ROWS ONLY
  """
    row = cursor.execute(qry+qry_offset, [schema, schema, last_ddl_time])
    while True:
      row = cursor.fetchone()
      if row is None:
          break
      object_id, object_name, owner, object_type, ddl = row
      i += 1
      ddl_str = ddl.read()
      dbg(f"object_name: {object_name}")
      print_fl(f"blob")
      print_fl(f"mark :{object_id}")
      print_fl(f"data {len(ddl_str)}")
      print_fl(ddl_str)
      file_list.append({"id":f"{object_id}", "name":f"{object_type}/{object_name}.sql"})
      if PROGRESS:
        print_fl(f"progress {i+2}/{total+2}")
  return file_list

def cmd_list():
  dbg("in func: cmd_list")
  print_fl(":object-format sha1")
  print_fl("? refs/heads/main")
  print_fl("@refs/heads/main HEAD")
  print_fl("")

def cmd_option_verbosity(params):
  global DEBUG, DEBUG_GIT_OUTPUT
  param_val = int(params)
  if param_val > 0:
    DEBUG = True
  if param_val > 1:
    DEBUG_GIT_OUTPUT = True
  print_fl("")

def cmd_option_progress(params):
  global PROGRESS
  dbg("in func: cmd_option_progress")
  dbg(f" progress: {params}")
  if params == "true":
    PROGRESS = True
  else:
    PROGRESS = False
  print_fl("")

def cmd_option(params):
  dbg("in func: cmd_option")
  if(params.startswith("verbosity")):
    params = int(params[len("verbosity "):])
    cmd_option_verbosity(params)
  elif(params.startswith("progress ")):
    params = params[len("progress "):]
    cmd_option_progress(params)
  else:
    print_fl("unsupported")

def cmd_capabilities():
  dbg("in func: cmd_capabilities")
  print_fl("import")
  print_fl("export")
  print_fl("refspec refs/heads/*:refs/heads/*")
  print_fl("option")
  print_fl("")

def cmd_import_MAIN(protocol, host, service_name, schema, port, username, password):
  global DATETIME_FORMAT, GIT_DIR
  dbg("in func: cmd_import")
  l = sys.stdin.readline()
  while l.startswith("import"):
    dbg("  %s" % l)
    l = sys.stdin.readline()

  print_fl("reset refs/heads/main")
  try:
    if CONNECT_AS_SYSDBA:
      connection = oracledb.connect(user=username, password=password, host=host, port=1521, service_name=service_name, mode=oracledb.AUTH_MODE_SYSDBA)
    else:
      connection = oracledb.connect(user=username, password=password, host=host, port=1521, service_name=service_name)
    dbg("connected")
    cursor = connection.cursor()
  except:
    git_credential_reject(protocol, host, username, password)
    raise
  git_credential_approve(protocol, host, username, password)
  
  last_ddl = None
  last_ddl_time = datetime.strptime("01.01.1900 00:00:00", DATETIME_FORMAT)
  last_ddl_path = os.path.abspath(f"{GIT_DIR}/../last_ddl")
  dbg(f"last_ddl_path: {last_ddl_path}")
  if os.path.isfile(last_ddl_path):
    with open(last_ddl_path, 'r') as f:
      last_ddl = f.read()
      last_ddl_time = datetime.strptime(last_ddl, DATETIME_FORMAT)
  dbg(f"last_ddl_time: {last_ddl_time}")

  if PROGRESS:
    print_fl(f"progress 1/?")
  
  utcnow = datetime.utcnow()
  formatted_datetime = utcnow.strftime(DATETIME_FORMAT)
  curr_time = round(time.time())
  
  str = f"{formatted_datetime}"
  print_fl(f"blob")
  print_fl(f"mark :1")
  print_fl(f"data {len(str)}")
  print_fl(str)
  
  file_list = create_file_list(cursor, schema, last_ddl_time)
  commit_block(curr_time, formatted_datetime, last_ddl)
  file_list.append({"id":"1", "name":"last_ddl"})
  
  print_file_list(file_list)
  print_deleted_file_list(get_deleted_file_list(cursor, schema))
  print_fl("")
  print_fl("done")
  print_fl("")
  dbg("end")
  sys.exit(0)

def main_cli():
  global GIT_DIR
  dbg("START")
  dbg(sys.argv)
  if(sys.argv):
    if(len(sys.argv)==3):
      url = sys.argv[2]
      protocol = "oracle"
      dbg(url)
      host_and_path = url[url.index('://')+3:]
      dbg(f"host_and_path: {host_and_path}")
      host_and_port = host_and_path[:host_and_path.index('/')]
      dbg(f"host_and_port: {host_and_port}")
      port = 1521
      try:
        port_pos = host_and_port.index(":")
        host = host_and_port[:port_pos]
        port = host_and_port[len(host)+1:]
      except ValueError:
        host = host_and_port
      dbg(f"host: {host}")
      dbg(f"port: {port}")
      service_and_schema = host_and_path[len(host_and_port)+1:]
      dbg(f"service_and_schema: {service_and_schema}")
      service, schema = service_and_schema.split('/')
      dbg(f"service: {service}")
      dbg(f"schema: {schema}")
      config = git_credential_fill(protocol, host)
      dbg(f"config: {config}")
      username = config["config"]["username"]
      password = config["config"]["password"]
      dbg(f"GIT_DIR: {GIT_DIR}")


      while True:
        cmd = sys.stdin.readline()
        cmd = cmd.strip()
        if len(cmd) > 0:
          dbg(f"< {cmd}")
          if(cmd == "capabilities"):
            cmd_capabilities()
          elif(cmd == "list"):
            cmd_list()
          elif(cmd.startswith("option")):
            params = cmd[len("option "):]
            cmd_option(params)
          elif(cmd == "import refs/heads/main"):
            cmd_import_MAIN(protocol=protocol,
            host=host,
            service_name=service,
            schema=schema,
            port=port,
            username=username,
            password=password)

if __name__ == "__main__":
  main_cli()