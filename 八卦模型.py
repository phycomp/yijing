from django.db.models import Model, CharField, ForeignKey
class 六十四卦(Model):
	本卦名=CharField(max_length=2)
	本卦組合=CharField(max_length=4)
	本卦數=CharField(max_length=6)
	錯卦名=CharField(max_length=2)
	錯卦數=CharField(max_length=6)
	綜卦名=CharField(max_length=2)
	綜卦數=CharField(max_length=6)
	複卦名=CharField(max_length=2)
	複卦數=CharField(max_length=6)
	雜卦名=CharField(max_length=2)
	雜卦數=CharField(max_length=6)
	UTF代碼=CharField(max_length=4)
	def __str__(self):return self.本卦名
	class Meta:
		db_table='六十四卦'

class 卦爻辭(Model):
	本卦=CharField(max_length=2)
	卦辭=CharField(max_length=100)
	卦辭彖曰=CharField(max_length=100)
	卦辭象曰=CharField(max_length=100)
	雜卦傳=CharField(max_length=100)
	序卦傳=CharField(max_length=100)
	卦辭文言曰=CharField(max_length=100)
	初爻辭=CharField(max_length=100)
	初爻象曰=CharField(max_length=100)
	#初爻彖曰=CharField(max_length=100)
	二爻辭=CharField(max_length=100)
	二爻象曰=CharField(max_length=100)
	#二爻彖曰=CharField(max_length=100)
	三爻辭=CharField(max_length=100)
	三爻象曰=CharField(max_length=100)
	#三爻彖曰=CharField(max_length=100)
	四爻辭=CharField(max_length=100)
	四爻象曰=CharField(max_length=100)
	#四爻彖曰=CharField(max_length=100)
	五爻辭=CharField(max_length=100)
	五爻象曰=CharField(max_length=100)
	#五爻彖曰=CharField(max_length=100)
	上爻辭=CharField(max_length=100)
	上爻象曰=CharField(max_length=100)
	#上爻彖曰=CharField(max_length=100)
	class Meta:
		db_table='卦爻辭'

'''
class 卦(Model):
    def Negation(self): return self.卦數.replace('1','x').replace('0','1').replace('x','0')
    def Opposite(self): return self.卦數[::-1]
    def Cross(self): return self.卦數[1:4]+self.卦數[2:5]
    def CrossOppo(self):
        self.卦數=self.Cross()
        return self.Opposite()
    卦名=CharField(max_length=2)
    卦數=CharField(max_length=6)
    初爻=CharField(max_length=100)
    二爻=CharField(max_length=100)
    三爻=CharField(max_length=100)
    四爻=CharField(max_length=100)
    五爻=CharField(max_length=100)
    上爻=CharField(max_length=100)
    錯=Negation(self)#ForeignKey('self')
    縱=Opposite(self)
    複=Cross(self)
    雜=OppoCross(self)
    文王曰=CharField(max_length=50)
    大象曰=CharField(max_length=50)
    彖曰=CharField(max_length=50)
    class Meta:
        db_table='六十四卦'
'''
