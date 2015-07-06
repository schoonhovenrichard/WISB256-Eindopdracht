from FiniteFields import *
from ElliptischeKrommen import *
import math
import itertools

def genFieldPol(mod, degree):
    """
    Generate a random polynomial of degree n and coefficients modulo some prime p.
    """
    ModP = IntegersModP(mod)
    Polynomial = PolynomialSpaceOver(ModP)
 
    while True:
        coefficients = [ModP(random.randint(0, mod-1)) for _ in range(degree)]
        randomMonicPolynomial = Polynomial(coefficients + [ModP(1)])
        return randomMonicPolynomial

def genCurvePoint(kromme):
    mod=kromme.a.prime
    degree=kromme.a.degree
    CurrentField=kromme.a.__class__
    counter=0
    while True:
        counter+=1
        xpol=genFieldPol(mod, degree)
        xpunt=CurrentField(xpol.coefficients)
        kwadraat=kromme.a*xpunt+xpunt**3+kromme.b
        for i in itertools.product(range(mod),repeat=degree):
            ylist=list(i)
            ypunt=CurrentField(ylist)
            if ypunt**2==kwadraat:
                return Punt(kromme, xpunt, ypunt)
        if counter>100:
            raise Exception("Maximum number of iterations exceeded!")

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def lcm(a,b): 
    return abs(a * b) / fractions.gcd(a,b) if a and b else 0

irred3=PolynomialSpaceOver(IntegersModP(5))([2,1,0,3,1])
irred=PolynomialSpaceOver(IntegersModP(5))([4,3,1,1])
irred2=PolynomialSpaceOver(IntegersModP(5))([3,0,1])
F35x = FiniteField(5, 3, irred)
F25x = FiniteField(5, 2, irred2)
F45x = FiniteField(5, 4, irred3)
curve = ElliptischeKromme(a=F25x([1]), b=F25x([1]))
curve2 = ElliptischeKromme(a=F35x([1]), b=F35x([1]))
curve3 = ElliptischeKromme(a=F45x([1]), b=F45x([1]))

def BabyStepGiantStepOnce(kromme):
    """
    Rudimentaire versie van Baby-Step-Giant-Step algoritme.
    """
    mod=kromme.a.prime
    degree=kromme.a.degree
#    CurrentField=kromme.a.__class__
    randompunt = genCurvePoint(kromme)
#    kwadraat=kromme.a*xpunt+xpunt**3+kromme.b
    m=math.ceil((mod**degree)**(1/4))
    puntlijst=[]
    for j in range(m):
        puntlijst.append(j*randompunt)
    L=1
    Q=(mod**degree+1)*randompunt
    index='unknown'
    tijdelijst=[]
    k=-1
    while True:
        k+=1
        punt2=Q+k*((2*m)*randompunt)
        tijdelijst.append(punt2)
        for j in range(len(puntlijst)):
            if puntlijst[j].x==punt2.x:
                if puntlijst[j].y==punt2.y:
                    index=[-j,k]
                    break
                if puntlijst[j].y==(-punt2).y:
                    index=[j,k]
                    break
            if isinstance(index,list):
                break
        if isinstance(index,list):
            break
    M=int(mod**degree+1+2*m*index[1]+index[0])
    factoren=prime_factors(M)
    factoren=list(set(factoren))
    i=0
    while i < (len(factoren)-1):
        if (M/factoren[i])-int(M/factoren[i])<1.0e-5:
            if (int(M/factoren[i])*randompunt).x=='infx':
                M=int(M/factoren[i])
            else:
                i+=1
    L=lcm(L,M)
    integerlist=list(range((mod**degree)+1-2*math.ceil(math.sqrt(mod**degree)),(mod**degree)+1+2*math.ceil(math.sqrt(mod**degree))))
    counter=0
    N = 'Nothing'
    for integer in integerlist:
        if integer % L == 0:
            N = integer
            counter += 1
    if counter > 1:
        return None
    else:
        return N

def BabyStepGiantStep(kromme):
    while True:
        resultaat = BabyStepGiantStepOnce(kromme)
        if isinstance(resultaat, int):
            return resultaat

resultaat = BabyStepGiantStep(curve)
resultaat2 = BabyStepGiantStep(curve2)
resultaat3 = BabyStepGiantStep(curve3)
print(resultaat)
print(resultaat2)
print(resultaat3)

def BSGScheck(kromme):
    mod=kromme.a.prime
    degree=kromme.a.degree
    CurrentField=kromme.a.__class__
    cardinaliteit = 1
    #vanwege infpoint
    for i in itertools.product(range(mod),repeat=degree):
        ylist=list(i)
        ypunt=CurrentField(ylist)
        for i in itertools.product(range(mod),repeat=degree):
            xlist=list(i)
            xpunt=CurrentField(xlist)
            getal = xpunt**3+kromme.a*xpunt+kromme.b-ypunt**2
            if len(getal.poly) == 1:
                if getal.poly.coefficients[0]==0:
                    cardinaliteit += 1
    return cardinaliteit
    
print(BSGScheck(curve),BSGScheck(curve2),BSGScheck(curve3))   