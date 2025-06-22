{
  description = "tremolisto: a collection of isolated guitar parts";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = nixpkgs.legacyPackages.${system};

        nativeBuildInputs = with pkgs; [
          just
        ];
        python = pkgs.python313;
        buildInputs = with pkgs; [
          python
          uv
          nodejs_22
          netlify-cli
        ];
      in {
        devShells.default = pkgs.mkShell {
          inherit nativeBuildInputs buildInputs;

          shellHook = ''
            export UV_PYTHON_PREFERENCE="only-system";
            export UV_PYTHON=${python}
          '';
        };
      }
    );
}
