{ self, root, pkgs, ... }:

{
  integrate.package.package = pkgs.stdenv.mkDerivation rec {
    pname = "truffle-cli";
    version = "0.1.0";

    src = root;

    nativeBuildInputs = with pkgs; [
      ccache
      makeWrapper
    ] ++ (self.lib.python.mkNativeBuildInputs pkgs);

    buildInputs = with pkgs; [
      zlib
    ];

    buildPhase = ''
      runHook preBuild
    
      mkdir -p artifacts
    
      DESCRIPTION=$(head -n 4 README.md | tail -n 2 | tr '\n' ' ')
    
      nuitka \
        --company-name='haras-unicorn' \
        --product-name='Truffle CLI' \
        --product-version='${version}' \
        --file-description="$DESCRIPTION" \
        --copyright='haras-unicorn' \
        --macos-create-app-bundle \
        --macos-app-name='Truffle CLI' \
        --macos-app-version='${version}' \
        --macos-app-mode='background' \
        --windows-console-mode='force' \
        --output-dir='artifacts' \
        --output-filename='truffle-cli' \
        --standalone \
        --jobs=''${NIX_BUILD_CORES} \
        'src/cli/src/truffle_cli/__init__.py'
    
      runHook postBuild
    '';

    installPhase = ''
      runHook preInstall
  
      mkdir -p $out/lib/truffle-cli
      cp -r artifacts/__init__.dist/* $out/lib/truffle-cli/

      mkdir -p $out/bin
      makeWrapper $out/lib/truffle-cli/truffle-cli $out/bin/truffle-cli \
        --set LD_LIBRARY_PATH "${pkgs.lib.makeLibraryPath buildInputs}" \
        --set TRUFFLE_CLI_ENVIRONMENT "production"

      chmod +x $out/bin/truffle-cli
    
      runHook postInstall
    '';

    meta = with pkgs.lib; {
      description =
        "A job hunting tool that forages through job boards"
        + ", using AI to uncover and score the most valuable opportunities"
        + " hidden beneath the surface.";
      homepage = "https://github.com/haras-unicorn/truffle";
      license = licenses.mit;
      maintainers = [ ];
      platforms = platforms.all;
    };
  };
}
