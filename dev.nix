{ pkgs, ... }: {
  # Use a stable Nix channel
  channel = "stable-23.11";
  # Packages to install
  packages = [
    pkgs.gitAndTools.git-lfs
    pkgs.python312
    pkgs.python3Packages.pip
    pkgs.python3Packages.virtualenv
  ];
  # Commands to run on workspace creation
  idx = {
    workspace = {
      onCreate = {
        # Create a virtual environment and install dependencies
        install = ''
          python3 -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt
        '';
      };
    };
    # Configure the preview for Django
    previews = {
      web = {
        command = ["python" "manage.py" "runserver" "0.0.0.0:8000"];
        manager = "web";
      };
    };
  };
}
