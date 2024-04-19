{
  description = "Guitar music list";

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
        buildInputs = with pkgs; [
          python312
          nodejs_21
          netlify-cli
        ];
      in {
        devShells.default = pkgs.mkShell {inherit nativeBuildInputs buildInputs;};
      }
    );
}
