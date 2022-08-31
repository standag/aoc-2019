import math

reactions_0 = """10 ORE => 10 A
7 A => 1 FUEL"""

reactions_1 = """10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL"""

reactions_2 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL"""

reactions_3 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT"""

reactions_4 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF"""

reactions_5 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

reactions_final = """7 FQPX => 7 GTJFL
4 PZFS, 1 PRZTG => 5 RZSK
2 DMBCB => 7 PMBWS
1 VLPSJ, 3 KVCJV, 5 FLKD => 8 RWJC
26 PMBWS, 7 RZSK => 9 BZRDP
1 NGDFS => 3 MJFN
1 RZSK, 1 PZFS => 4 DMBCB
7 FLKD => 2 GHKNL
3 PQXG, 4 TQLVN, 25 QBMH => 9 XLKT
2 NGDFS => 2 HSBGQ
5 GZHT => 3 KMJG
15 JKFDL, 8 QZCMZ, 11 CMRGJ, 5 GZHT, 1 GBWRP, 22 LNLK, 6 KMJG => 9 DMTFB
1 RZSK, 4 QBMH => 4 DQNSB
1 RVFS, 9 RBCNF => 6 ZBTS
4 ZBTS => 4 PZFS
5 VZWX, 1 PRZTG => 7 KVCJV
18 QBMH => 2 VHDR
28 GTJFL, 1 KVCJV => 5 VLPSJ
6 KVCJV, 9 SFRH => 4 QFDR
1 LNLK => 8 TQLVN
1 QCDVW, 9 JXFRT, 2 SFRH => 8 QZCMZ
5 VBJM, 3 LNLK => 6 PRZTG
127 ORE => 4 RVFS
3 XBMFG => 1 GBWRP
1 VBJM, 7 QBMH => 8 JKFDL
5 GDSXB, 27 KMJG, 32 PMBWS, 1 QSLP, 46 DMTFB, 1 VHDR, 1 WDFD, 7 GHKNL => 1 FUEL
1 RPXDF => 6 QCDVW
16 CMRGJ, 1 FQPX, 2 KMJG, 9 HSBGQ, 2 JXFRT, 5 GBWRP => 8 QSLP
6 TQLVN, 3 BZRDP => 5 GNFB
1 FNZRZ, 1 VZWX, 1 BZRDP => 9 GQWP
3 ZWJFT, 2 HSBGQ => 8 JXFRT
4 PQXG, 11 JKFDL, 6 DQNSB => 9 RPXDF
41 GCPK => 8 VQXV
18 DQNSB => 7 FLKD
5 LNLK => 4 NGDFS
29 RZCPW, 3 VXSLT => 9 CMRGJ
1 LNLK, 2 VBJM, 5 ZBTS => 8 VZWX
2 QFDR => 4 RZCPW
3 MJFN, 23 VHDR, 17 FLKD => 5 GZHT
8 TQLVN, 2 JKFDL => 7 FNZRZ
1 ZWJFT => 1 RJCQP
1 KVCJV => 2 SFRH
102 ORE => 3 RBCNF
174 ORE => 8 GCPK
24 VLPSJ, 4 FLKD => 4 XBMFG
2 JKFDL => 7 PQXG
1 VZWX, 10 PZFS => 3 FQPX
4 QZCMZ, 1 GZHT, 1 DQNSB, 12 RJCQP, 1 ZKTW, 1 GQWP, 6 SFRH, 10 VHDR => 1 WDFD
3 KVCJV, 27 DMBCB => 3 ZKTW
14 GNFB => 9 ZWJFT
4 RCKBT, 2 GCPK => 2 VBJM
1 RVFS, 16 RBCNF => 9 LNLK
7 HSBGQ, 8 RWJC, 2 JXFRT => 3 VXSLT
1 RBCNF, 2 RZSK, 1 VQXV => 9 QBMH
12 KMJG, 3 XLKT => 8 GDSXB
194 ORE => 9 RCKBT"""

def parse_reactions(reactions):
    reaction_map = {}
    for reaction in reactions.split("\n"):
        left, right = reaction.split("=>")
        amount, product = right.split()
        ingrediences = left.split(",")
        reaction_map[product] = [int(amount)] + [
            (ingrediance.split()[1], int(ingrediance.split()[0]))
            for ingrediance in ingrediences
        ]
    return reaction_map


class Reactor:
    def __init__(self, reactions):
        self.reactions = reactions
        self.rests = {}

    def get_ore(self, product, amount):
        if product == "ORE":
            # print(f">> {amount} ORE")
            return amount
        if self.rests.get(product, 0) >= amount:
            self.rests[product] -= amount
            return 0
        x = math.ceil(amount / self.reactions[product][0])
        self.rests[product] = self.rests.get(product, 0) + (
            self.reactions[product][0] * x - amount
        )
        # print(self.rests)
        # print([f"{x*a}*{p}" for p, a in self.reactions[product][1:]])
        return sum(self.get_ore(p, x * a) for p, a in self.reactions[product][1:])

    def reuse_rests(self, product=None):
        if product is None:
            rests = [(p, a) for p, a in self.rests.items()]
            return sum(self.reuse_rests(p) for p, a in rests if a > 0)
        else:
            if product == "ORE":
                ore = self.rests[product]
                self.rests[product] = 0
                return ore
            elif self.rests[product] >= self.reactions[product][0]:
                x = self.rests[product] // self.reactions[product][0]
                reactants = []
                for reactant in self.reactions[product][1:]:
                    self.rests[reactant[0]] = self.rests.get(reactant[0], 0) + reactant[1] * x
                    reactants.append(reactant[0])
                self.rests[product] -= x * self.reactions[product][0]
                # print(reactants)
                return sum(self.reuse_rests(p) for p in reactants)
            return 0

def test_test_0():
    reactions = {"FUEL": [1, ("A", 14)], "A": [10, ("ORE", 10)]}
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1)
    assert x == 20
    assert reactor.rests["A"] == 6


def test_test_1():
    reactions = {
        "FUEL": [1, ("A", 7), ("B", 1)],
        "B": [1, ("A", 3), ("ORE", 5)],
        "A": [10, ("ORE", 10)],
    }
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1)
    assert x == 15
    assert reactor.rests["A"] == 0


def test_test_2():
    reactions = parse_reactions(reactions_1)
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1)
    assert x == 31


def test_test_3():
    reactions = parse_reactions(reactions_2)
    reactor = Reactor(reactions)
    # x = reactor.get_ore("AB", 2)
    # assert x == 51
    # reactor.rests = {}
    # x = reactor.get_ore("CA", 4)
    # assert x == 46
    # reactor.rests = {}
    x = reactor.get_ore("FUEL", 1) - reactor.reuse_rests()
    assert x == 165

def test_test_4():
    reactions = parse_reactions(reactions_3)
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1) - reactor.reuse_rests()
    assert x == 13312

def test_test_5():
    reactions = parse_reactions(reactions_4)
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1) - reactor.reuse_rests()
    print()
    print(reactor.rests)
    assert x == 180697

def test_test_6():
    reactions = parse_reactions(reactions_5)
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1) - reactor.reuse_rests()
    assert x == 2210736

def test_test_7():
    reactions = parse_reactions(reactions_1)
    reactor = Reactor(reactions)
    reactor.rests["FUEL"] = 1000000000000
    x = reactor.reuse_rests("FUEL")
    assert x == 82892753

def main():
    reactions = parse_reactions(reactions_final)
    reactor = Reactor(reactions)
    x = reactor.get_ore("FUEL", 1) - reactor.reuse_rests()
    print(x)
    ore = 1000000000000
    est = ore//x+877300
    real = 0
    for i in range(est, est+5000):
        reactor.rests = {}
        real_ore = reactor.get_ore("FUEL", i) - reactor.reuse_rests()
        if real_ore >= ore:
            break
        real = i
        print(i, real_ore)

    print(f">> {real}")


if __name__ == "__main__":
    main()
