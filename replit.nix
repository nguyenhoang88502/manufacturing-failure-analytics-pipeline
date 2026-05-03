{pkgs}: {
  deps = [
    pkgs.mesa
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrandr
    pkgs.xorg.libXfixes
    pkgs.xorg.libXdamage
    pkgs.xorg.libXcomposite
    pkgs.nspr
    pkgs.nss
  ];
}
