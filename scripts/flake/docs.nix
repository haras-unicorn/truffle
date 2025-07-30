{ pkgs, ... }:

{
  seal.defaults.devShell = "dev";
  integrate.devShell.devShell = pkgs.mkShell {
    packages = with pkgs; [
      git
      just
      nushell
      mdbook
    ];
  };
}
