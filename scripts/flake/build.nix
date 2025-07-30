{ self, pkgs, ... }:

{
  integrate.devShell.devShell = pkgs.mkShell {
    inputsFrom = [
      (self.lib.python.mkDevShell pkgs)
    ];
    packages = with pkgs; [
      ccache
    ];
  };
}

