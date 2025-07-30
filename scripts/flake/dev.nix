{ self, pkgs, ... }:

{
  seal.defaults.devShell = "dev";
  integrate.devShell.devShell = pkgs.mkShell rec {
    LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath buildInputs}";

    inputsFrom = [
      (self.lib.python.mkDevShell pkgs)
    ];

    buildInputs = with pkgs; [
      zlib
    ];

    packages = with pkgs; [
      git
      just
      nushell
      nil
      nixpkgs-fmt
      marksman
      markdownlint-cli
      nodePackages.markdown-link-check
      fd
      nodePackages.prettier
      nodePackages.yaml-language-server
      nodePackages.vscode-langservers-extracted
      taplo
      nodePackages.cspell
      mdbook
      ccache
    ];
  };
}
