import math
import fractions
frac = fractions.Fraction

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b%a, a)
        return (g, x-(b//a)*y, y)

def IntegersModP(p):
    class IntegerModP(object):
        def __init__(self, n):
            self.n = n % p
            self.field = IntegerModP
            self.p=p
        
        def __neg__(self): 
            return IntegerModP(-self.n)

        def __repr__(self): 
            return '%d (mod %d)' % (self.n, self.p)
        
        def __str__(self): 
            return str(self.n)
        
        def __add__(self, other):
            return IntegerModP(self.n + other.n)
            
        def __radd__(self, other):
            return self+other
            
        def __sub__(self, other): 
            return IntegerModP(self.n + (-other.n))
        
        def __rsub__(self, other):
            return (-self)+other
 
        def __mul__(self, other): 
            return IntegerModP(self.n * other.n)
            
        def __rmul__(self, other):
            return self*other
        
        def __eq__(self, other):
            if isinstance(other, int):
                tempint=IntegerModP(other)
                if self.n==tempint.n and isinstance(tempint, IntegerModP)==True:
                    return True
                else:
                    return False
            if isinstance(self, int):
                tempint=IntegerModP(self)
                if self.n==tempint.n and isinstance(tempint, IntegerModP)==True:
                    return True
                else:
                    return False
            if self.n==other.n and isinstance(other, IntegerModP)==True:
                return True
            else:
                return False
        
        def __abs__(self): 
            return abs(self.n)
            
        def __divmod__(self, div):
            geheel=divmod(self.n,div.n)[0]
            remainder=divmod(self.n,div.n)[1]
            return (IntegerModP(geheel), IntegerModP(remainder))
            
        def modinverse(self):
            gcd, x, y = egcd(self.n, self.p)
            if gcd != 1:
                return None  # modular inverse does not exist
            else:
                return IntegerModP(x % self.p)

        def __truediv__(self, other): 
            return self * other.modinverse()

        def __rtruediv__(self, other): 
            return self.modinverse() * other
            
        def __div__(self, other): 
            return self.__truediv__(other)

        def __rdiv__(self, other): 
            return self.__rtruediv__(other)
        
        def __mod__(self, other):
            if isinstance(other, int):
                tempint=IntegerModP(other)
                return IntegerModP(self.n % tempint.n)
            return IntegerModP(self.n % other.n)
        
        def __rmod__(self, other):
            if isinstance(other, int):
                tempint=IntegerModP(other)
                return IntegerModP(tempint.n % self.n)
            return IntegerModP(other.n % self.n)
        
        def __gt__(self, other):
            if isinstance(other, int):
                tempint=IntegerModP(other)
                return self.n>tempint.n
            return self.n>other.n
                    
            

    IntegerModP.p = p
    IntegerModP.__name__ = 'Z/%d' % (p)
    return IntegerModP

def addlist(lijst1,lijst2):
    """
    Function that adds lists
    """
    if len(lijst1) > len(lijst2):
        newlijst = [i for i in lijst1]
        for i in range(len(lijst2)): 
            newlijst[i] += lijst2[i]
    else:
        newlijst = [i for i in lijst2]
        for i in range(len(lijst1)): 
            newlijst[i] += lijst1[i]
    return newlijst


def mult_oneterm(poly,c,i):
    """
    Return a new list of polynomial coefficients corresponding to the product of the 
    input polynomial p with the term c*x^i
    """
    newlijst = [0]*i # increment the list with i zeros
    for coef in poly: 
        newlijst.append(coef*c)
    return newlijst

def multiply(lijst1,lijst2):
    """
    Function that returns the coefficients of the polynomial resulting from multiplying
    two polynomials.
    """
    if len(lijst1) > len(lijst2): 
        shortlijst=lijst2
        longlijst=lijst1
    else: 
        shortlijst=lijst1
        longlijst=lijst2
    newlijst = []
    for i in range(len(shortlijst)): 
        newlijst = addlist(newlijst, mult_oneterm(longlijst, shortlijst[i], i))
    return newlijst

def removezeroes(poly):
    """
    Removes the unnecessary zeroes at the end of a list of coefficients.
    """
    while poly[-1]==0 and len(poly)>0:
        poly.pop()
        if len(poly)==0:
            break
    if poly == []:
        poly.append(0)

def longdiv(lijst1,lijst2):
    """
    Algorithm that performs long division for polynomials once. See wikipedia for the pseudo code.
    The input is a tuple of two lists.
    """
    if len(lijst1)<len(lijst2):
        return [0], lijst1
    remainder=[i for i in lijst1]
    removezeroes(remainder)
    quotient=[0]
    while remainder!=[0] and len(remainder)>=len(lijst2):
        for i in range(len(lijst1)-len(quotient)):
            quotient.append(0)
        t=remainder[-1]/lijst2[-1]
        power=len(remainder)-len(lijst2)
        quotient[power]=quotient[power]+t
        subtract=[i for i in lijst2]
        for i in range(power):
            subtract.insert(0,0)
        for i in range(len(remainder)):
            remainder[i]=remainder[i]-t*subtract[i]
        removezeroes(remainder)
        removezeroes(quotient)
    return quotient, remainder

def PolynomialSpaceOver(field=frac):
    class Polynomial(object):
        factory = lambda L: Polynomial([field(x) for x in L])
        
        def __init__(self,coefficients):
            self.coefficients=coefficients
            
        def ZeroPol(self): 
            return self.coefficients == []
        
        def __repr__(self):
            if self.ZeroPol():
                return '0'
            if len(self.coefficients)==1:
                return str(self.coefficients[0])
            else:
                lijstje=[]
                if self.coefficients[0]!=0:
                    lijstje.append(str(self.coefficients[0]))
                if self.coefficients[1]!=0:
                    if self.coefficients[1]==1:
                        lijstje.append("x")
                    else:
                        lijstje.append(str(self.coefficients[1])+"x")
                for i in range(2,len(self.coefficients)):
                    if self.coefficients[i]==1:
                        term="x^%d" % i
                        lijstje.append(term)
                    elif self.coefficients[i]>1:
                        term=str(self.coefficients[i])+"x^%d" % i
                        lijstje.append(term)
                return " + ".join(lijstje)

        def __len__(self): 
            return len(self.coefficients)
        
        def __neg__(self):
            newcoeff=[]
            for i in self.coefficients:
                newcoeff.append(-i)
            return Polynomial(newcoeff)
        
        def degree(self):
            return len(self.coefficients)-1
        
        def __eq__(self, other):
            if self.degree()!=other.degree():
                return False
            checklijst=[]
            for i in range(len(self.coefficients)):
                checklijst.append(self.coefficients[i]==other.coefficients[i])
            if all(checklijst):
                return True
            else:
                return False
                
        def __add__(self, other):
            newcoeffic=addlist(self.coefficients,other.coefficients)
            return Polynomial(newcoeffic)
        
        def __radd__(self, other):
            return self+other

        def __sub__(self, other): 
            return self + (-other)
        
        def __rsub__(self, other):
            return (-self)+other
        
        def __mul__(self, other):
            if self.ZeroPol() or other.ZeroPol():
                return ZeroPol()
            newcoeffic=multiply(self.coefficients,other.coefficients)
            return Polynomial(newcoeffic)
        
        def __rmul__(self, other):
            return self*other
        
        def __divmod__(self, other):
            listtuple=longdiv(self.coefficients,other.coefficients)
            return listtuple[0], listtuple[1]
        
        def __truediv__(self, other): 
            quotient, remainder = divmod(self,other)
            if remainder==[0]:
                return Polynomial(quotient)
            else:
                raise Exception("The polynomial %s is not divisible by %s!" % (self,other))

        def __rtruediv__(self, other): 
            quotient, remainder = divmod(other,self)
            if remainder==[0]:
                return Polynomial(quotient)
            else:
                raise Exception("The polynomial %s is not divisible by %s!" % (other,self))
            
        def __div__(self, other): 
            return self.__truediv__(other)

        def __rdiv__(self, other): 
            return self.__rtruediv__(other)
            
    def ZeroPol():
        return Polynomial([])
    
    Polynomial.field = field
    Polynomial.__name__ = '(%s)[x]' % field.__name__
    return Polynomial

#pol3=PolynomialSpaceOver()
#fun1=pol3([1,2,3])
#fun2=pol3([1,2,3])
#fun3=pol3([1,2])
#fun4=pol3([1,4,5])
#fun5=pol3([1,4,4])
#print(fun1==fun2,fun1==fun3,fun1==fun4)
#print(fun1+fun3,"   ",fun1+fun2,"   ",fun3+fun4)
#print(fun3*fun3,"   ",fun1*fun3,"   ",fun4*fun4)

#testdiv1=[1,2]
#testdiv2=[2,3,2]
#testdiv3=[4,5,1,2]
#testdiv4=[8]
#print(longdiv(testdiv2,testdiv1),"   ",longdiv(testdiv3,testdiv1),"   ",longdiv(testdiv3,testdiv2),"   ",longdiv(testdiv3,testdiv4))
#print(divmod(fun1,fun3),"   ",longdiv([1,2,3],[1,2]))
#print(fun1/fun2,"   ",fun5/fun3)

"""
PolyOverQ=PolynomialSpaceOver().factory
Mod5 = IntegersModP(5)
polysMod5 = PolynomialSpaceOver(Mod5).factory
Mod11 = IntegersModP(11)
polysMod11 = PolynomialSpaceOver(Mod11).factory
print(pol3([1,7,49]) / pol3([7]))
print(PolyOverQ([1,7,49]) / PolyOverQ([7]))
print(polysMod5([1,6,2,4,7,1]))
print(polysMod5([1,7,49]) / polysMod5([7]))
print(polysMod11([1,7,49]) / polysMod11([7]))
"""