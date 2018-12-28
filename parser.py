

def readDomains(domtxt):
    domains = []
    f = open(domtxt, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split()
        domains.append({
            "name" : "D" + tokens[0],
            "nbValues" : tokens[1],
            "values" : tokens[2:],
        })
    return domains

def readVariables(vartxt):
    variables = []
    f = open(vartxt, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split()
        v = {
            "name" : "X" + tokens[0],
            "domain" : "D" + tokens[1],
        }
        try:
            v["initial"] = tokens[2]
            v["mobility"] = tokens[4]
        except IndexError:
            pass
        variables.append(v)
    return variables

def readConstraints(ctrtxt):
    constraints = []
    f = open(ctrtxt, 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        tokens = line.split()
        constraints.append({
            "variable1" : "X" + tokens[0],
            "variable2" : "X" + tokens[1],
            "type" : tokens[2],
            "operation" : tokens[3],
            "constant" : tokens[4],
        })
    return constraints

def generateDomains(dom):
    out = '<domains nbDomains="{0}">\n'.format(len(dom))
    for d in dom:
        out += '\t<domain name="{0}" nbValues="{1}">{2}</domain>\n'.format(
            d['name'], d['nbValues'], " ".join(d['values'])
        )
    out += "</domains>\n"
    return out

def generateAgents(var):
    out = '<agents nbAgents="{0}">\n'.format(len(var))
    for v in var:
        out += '\t<agent name="A{0}" />\n'.format(v['name'])
    out += '</agents>\n'
    return out

def generateVariables(var):
    out = '<variables nbVariables="{0}">\n'.format(len(var))
    for v in var:
        out += '\t<variable name="{0}" domain="{1}" agent="A{0}" />\n'.format(
            v['name'], v['domain']
        )
    out += "</variables>\n"
    return out

predicates = """
<predicates nbPredicates="2">
    <predicate name="EQ">
        <parameters> int P1 int P2 int CONST </parameters>
        <expression>
        <functional> eq(abs(sub(P1, P2)), CONST) </functional>
        </expression>
    </predicate>
        <predicate name="GE">
        <parameters> int P1 int P2 int CONST </parameters>
        <expression>
        <functional> ge(abs(sub(X1, X2)), CONST) </functional>
        </expression>
    </predicate>
</predicates>
"""

def generateConstraints(ctr):
    out = predicates + '\n\n'
    out += '<constraints nbConstraints="{0}">\n'.format(len(ctr))
    for c in ctr:
        pred = "EQ" if c['operation'] == "=" else "GE"
        out += \
"""\t<constraint name="{0}_{1}_{2}" arity="3" scope="{1} {2}" reference="{0}" >
\t\t<parameters> {1} {2} {3} </parameters>
\t</constraint>\n""" \
        .format(pred, c['variable1'], c['variable2'], c['constant'])

    out += "</constraints>\n"
    return out


def generateXCSP(dom, var, ctr):
    out = '<instance>\n'
    out += '<presentation name="sampleProblem" maxConstraintArity="3" maximize="false" format="XCSP 2.1_FRODO" />\n'
    out += generateDomains(dom)
    out += generateAgents(var)
    out += generateVariables(var)
    out += generateConstraints(ctr)
    out += '</instance>'
    return out

if __name__ == "__main__":
    dom = readDomains('FullRLFAP/CELAR/scen01/dom.txt')
    var = readVariables('FullRLFAP/CELAR/scen01/var.txt')
    ctr = readConstraints('FullRLFAP/CELAR/scen01/ctr.txt')

    f = open('test.xml', 'w')
    f.write(generateXCSP(dom, var, ctr))
    f.close()
