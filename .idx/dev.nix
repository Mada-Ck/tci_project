{ pkgs, ... }: {
  # Use a stable Nixpkgs channel
  channel = "stable-24.11";

  # Packages for Django
  packages = [
    pkgs.python311          # Python 3.11
    pkgs.python311Packages.pip  # Pip for installing Python packages
    pkgs.python311Packages.virtualenv  # Virtualenv for isolated environments
    pkgs.git                # Git for version control
  ];

  # Environment variables (optional)
  env = {
    PYTHONPATH = "";        # Clear PYTHONPATH to avoid conflicts
    DJANGO_SETTINGS_MODULE = "tci_project.settings";  # Adjust if your settings module differs
  };

  # Install dependencies on workspace creation
  idx.workspace.onCreate = {
    install = ''
      python -m venv .venv
      source .venv/bin/activate
      pip install -r requirements.txt
    '';
  };

  # Start the Django server when the workspace starts (optional)
  idx.workspace.onStart = {
    run-server = "python manage.py runserver 0.0.0.0:8000 &";
  };

  # Enable previews for Django
  idx.previews = {
    enable = true;
    previews = {
      web = {
        command = [ "python" "manage.py" "runserver" "0.0.0.0:$PORT" ];
        manager = "web";
      };
    };
  };
}