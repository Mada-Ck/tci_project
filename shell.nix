{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "tci_project_env";

  buildInputs = with pkgs; [
    python311
    python311Packages.pip
    python311Packages.virtualenv
    python311Packages.django
    python311Packages.requests
    python311Packages.python-decouple
    direnv
  ];

  shellHook = ''
    if [ -f .env ]; then
      set -a
      source .env
      set +a
    fi

    if [ ! -d .venv ]; then
      python -m venv .venv
    fi
    
    source .venv/Scripts/activate

    if [ -f requirements.txt ]; then
      pip install -r requirements.txt
    fi

    echo "Django development environment is ready!"
  '';
}

{
    "terminal.integrated.profiles.windows": {
        "PowerShell": {
            "source": "PowerShell",
            "args": ["-NoLogo"]
        }
    },
    "terminal.integrated.defaultProfile.windows": "PowerShell"
}
