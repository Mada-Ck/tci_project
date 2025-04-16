{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    pkgs.python311
    pkgs.postgresql
    pkgs.nodejs
  ];

  shellHook = ''
    export PYTHONPATH=$PWD
    export PGDATA=$PWD/postgres_data
    export PGHOST=localhost
    export PGUSER=postgres
    export PGPASSWORD=postgres

    if [ ! -d $PGDATA ]; then
      initdb --no-locale --encoding=UTF8
    fi

    pg_ctl start
  '';
}
