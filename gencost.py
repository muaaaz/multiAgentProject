import os
import mas


def eqCost(F1, F2, K):
    return abs(abs(F1 - F2) - K)


def geCost(F1, F2, K):
    return max(K - abs(F1 - F2) + 1, 0)


def genCost(dom, var, ctr, destination="cost"):
    for c in ctr:
        op = c["operation"]
        K = c["constant"]
        v1name = c["variable1"]
        v2name = c["variable2"]
        d1name, d2name = 0, 0
        for v in var:
            if v["name"] == v1name:
                d1name = v["domain"]
            if v["name"] == v2name:
                d2name = v["domain"]
            if d1name and d2name:
                break
        assert d1name and d2name, "domains not found"
        d1, d2 = 0, 0
        for d in dom:
            if d["name"] == d1name:
                d1 = d
            if d["name"] == d2name:
                d2 = d
            if d1 and d2:
                break
        assert d1 and d2, "domains not found 2"

        # generate constraint table
        csv = "{0}, {1}, cost({2}{3})\n".format(v1name, v2name, op, K)

        for F1 in d1["values"]:
            for F2 in d2["values"]:
                if op == "=":
                    cost = eqCost(int(F1), int(F2), int(K))
                elif op == ">":
                    cost = geCost(int(F1), int(F2), int(K))
                csv += "{0}, {1}, {2}\n".format(F1, F2, cost)

        # save csv file
        filename = "{0}/{1}{2}{3}{4}.csv".format(
            destination, v1name, v2name, "eq" if op == "=" else "ge", K)
        f = open(filename, "w")
        f.write(csv)
        f.close()


if __name__ == "__main__":
    problemPath = "sample"
    dom = mas.readDomains(os.path.join(problemPath, 'dom.txt'))
    var = mas.readVariables(os.path.join(problemPath, 'var.txt'))
    ctr = mas.readConstraints(os.path.join(problemPath, 'ctr.txt'))
    genCost(dom, var, ctr)
