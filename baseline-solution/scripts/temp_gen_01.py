import zlib, base64

def get_falstad_url(text: str) -> str:
    compressed = zlib.compress(text.encode("utf-8"), level=9)
    encoded = base64.b64encode(compressed, altchars=b"-_").rstrip(b"=").decode()
    return f"https://www.falstad.com/circuit/circuitjs.html#{encoded}"

# Falstad netlist for Bridge Rectifier
# Components: 
# AC source + Transformer (modelled as AC source 170V 60Hz)
# D1, D2, D3, D4 (Bridge)
# R = 1k
falstad_netlist = """\
$ 1 5e-6 10.2 50 5 43 5e-11
v 128 304 128 144 0 1 60 170 0 0 0.5
w 128 144 256 144 0
w 128 304 256 304 0
d 256 144 320 80 2 default
d 256 304 320 80 2 default
d 320 224 256 144 2 default
d 320 224 256 304 2 default
w 320 80 400 80 0
r 400 80 400 224 0 1000
w 400 224 320 224 0
g 320 224 320 256 0 0
"""

# LTSpice netlist
# 01-gemini-2.0-flash-bridge-rectifier.cir
spice_netlist = """\
* Bridge Rectifier
V1 AC_TOP AC_BOT SINE(0 170 60)
D1 AC_TOP DC_PLUS D
D2 DC_MINUS AC_TOP D
D3 AC_BOT DC_PLUS D
D4 DC_MINUS AC_BOT D
R1 DC_PLUS DC_MINUS 1k
.model D D
.tran 0 0.1 0 1m
.end
"""

if __name__ == "__main__":
    print("FALSTAD_URL=" + get_falstad_url(falstad_netlist))
    
    with open("baseline-solution/simulations/01-gemini-2.0-flash-bridge-rectifier.cir", "w") as f:
        f.write(spice_netlist)
    print("SPICE_FILE_CREATED")
