import hashlib

mdp1 = "password123"
mdp2 = "securepass456"
mdp3 = "driverpass789"
mdp4 = "adminpass321"
mdp5 = "custpass654"


sel1 = "9a7fc02853c99c560238517027351d7deb7efeb2097686bd565c59bdaf059af6"
sel2 = "776e37cc088064e6aef5cd504181f07e83ab5e495e724a5a492f0b495cec3e1c"
sel3 = "5002971dd49c959b140e1ad3576cdd34be96c3ccab3fbc355009934f89137111"
sel4 = "2e5f3c0cb2d589bfd83ce56fb9f0d1ae608d5ba2656ecd869e45a8de62194c40"
sel5 = "76b132d093f2081b52c12bf8bd9add1c857fd1a4d924093b170c8c7acad1df25"

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


mdp_test = "soleil1234"
sel_test = "jambon"

final_test = hashlib.sha256((mdp_test + sel_test).encode()).hexdigest()
print(final_test)
