
import os
from mas import *

predicates01 = """
<predicates nbPredicates="3">
    <predicate name="EQ">
        <parameters> int F1 int F2 int K </parameters>
        <expression>
        <functional> min(1, abs(sub(abs(sub(F1, F2)), K))) </functional>
        </expression>
    </predicate>
    <predicate name="GE">
        <parameters> int F1 int F2 int K </parameters>
        <expression>
        <functional> max(min(1, add(sub(K, abs(sub(F1, F2))), 1)), 0) </functional>
        </expression>
    </predicate>
</predicates>
"""


def generateConstraints01(ctr, var=[]):
    out = predicates01 + '\n\n'
    out += '<constraints nbConstraints="{0}">\n'.format(len(ctr))
    ctr_pairs = set([])
    for c in ctr:
        ctr_pairs.add(c['variable1']+c['variable2'])  # save the pairs
        pred = "EQ" if c['operation'] == "=" else "GE"
        out += \
            """\t<constraint name="{0}_{1}_{2}" arity="2" scope="{1} {2}" reference="{0}" >
\t\t<parameters> {1} {2} {3} </parameters>
\t</constraint>\n""" \
        .format(pred, c['variable1'], c['variable2'], c['constant'])

    out += '\n'

    # generate alpha constraints
    for v in var:
        out += \
            """\t<constraint name="ALPHA_{0}" arity="1" scope="{0}" reference="ALPHA" >
\t\t<parameters> {0} </parameters>
\t</constraint>\n""" \
        .format(v["name"])

    out += "</constraints>\n"
    return out


def generateXCSP01(dom, var, ctr):
    out = '<instance>\n'
    out += '<presentation name="sampleProblem" maxConstraintArity="2" maximize="false" format="XCSP 2.1_FRODO" />\n'
    out += generateDomains(dom)
    out += generateAgents(var)
    out += generateVariables(var)
    out += generateConstraints01(ctr)  # , var)
    out += '</instance>'
    return out


def GenXML(problemPath, outputXML='test.xml'):
    dom = readDomains(os.path.join(problemPath, 'dom.txt'))
    var = readVariables(os.path.join(problemPath, 'var.txt'))
    ctr = readConstraints(os.path.join(problemPath, 'ctr.txt'))
    f = open(outputXML, 'w')
    f.write(generateXCSP01(dom, var, ctr))
    f.close()


if __name__ == "__main__":
    for probName in os.listdir('FullRLFAP/CELAR/'):
        if os.path.isdir('FullRLFAP/CELAR/{0}'.format(probName)):
            GenXML('FullRLFAP/CELAR/{0}'.format(probName),
                'xml01/{0}.xml'.format(probName))
