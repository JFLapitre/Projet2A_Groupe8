import hashlib

mdp1 = "password123"
mdp2 = "securepass456"
mdp3 = "driverpass789"
mdp4 = "adminpass321"
mdp5 = "custpass654"

sel1 = "8629ebd9cc97a7a11af893ade5f9f1ab373484a613b5237a160cb76a8820b3a9b9f8c1d4a5e6f7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6f7081920a1b2c3d4e51fec21b51198f7711f8ab306962547675874fc39e0e3a9687c6b5d091fb"
sel2 = "c2597f07f7647f314ca4c9c0ca3f6d2bf27daad9d4360611676d47cae4119b2a3c4d5e6f7081920a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6194bcdc1928974985f8c52871c05a886624eefbef7ac28cc4f1a693f3bd0"
sel3 = "71479647e7ea0dc9f1e828a8c121d028ca73d12e0f9f7325fcf40e5b66cdd9a8b7c6d5e4f3a2910b1c2d3e4f506172839405162738495061728394056053c00d54478e2915af1d6def54bb5084ea23f384a585a67b344cf57d95"
sel4 = "30a0d4e4e8764eb2c7be1decfb651a806611800bcd4f0b884ed2a6c31c4182b3c4d5e6f7081920a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e6cb25ed63493527b53feb236692df9d6f3ced0559242a69b1b6abf9ae8a83"
sel5 = "f83e054b4fb6babf266f59deed0e2d65c2d8c27b8dee231e4aa0f10de4519b2a3c4d5e6f7081920a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8091a2b3c4d5e68adf8adcb30f50a547a321e2db99bb63ea4bac0af9fee4e0483c043cd146"

final1 = hashlib.sha256((mdp1 + sel1).encode()).hexdigest()
final2 = hashlib.sha256((mdp2 + sel2).encode()).hexdigest()
final3 = hashlib.sha256((mdp3 + sel3).encode()).hexdigest()
final4 = hashlib.sha256((mdp4 + sel4).encode()).hexdigest()
final5 = hashlib.sha256((mdp5 + sel5).encode()).hexdigest()

print(final1)
print(final2)
print(final3)
print(final4)
print(final5)
