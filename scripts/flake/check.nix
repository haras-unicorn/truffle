{ self, pkgs, ... }:

{
  integrate.devShell.devShell = pkgs.mkShell {
    inputsFrom = [
      (self.lib.python.mkDevShell pkgs)
    ];
    packages = with pkgs; [
      git
      just
      nushell
      nixpkgs-fmt
      markdownlint-cli
      nodePackages.markdown-link-check
      fd
      nodePackages.prettier
      nodePackages.cspell
    ];
  };
}
