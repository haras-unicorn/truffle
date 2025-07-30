{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/release-25.05";

    perch.url = "github:altibiz/perch/refs/tags/2.2.1";
    perch.inputs.nixpkgs.follows = "nixpkgs";

    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";

    uv2nix.url = "github:pyproject-nix/uv2nix";
    uv2nix.inputs.pyproject-nix.follows = "pyproject-nix";
    uv2nix.inputs.nixpkgs.follows = "nixpkgs";

    pyproject-build-systems.url = "github:pyproject-nix/build-system-pkgs";
    pyproject-build-systems.inputs.pyproject-nix.follows = "pyproject-nix";
    pyproject-build-systems.inputs.uv2nix.follows = "uv2nix";
    pyproject-build-systems.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { nixpkgs, perch, ... }@inputs:
    perch.lib.flake.make {
      inherit inputs;
      root = ./.;
      prefix = "scripts/flake";
    };
}
