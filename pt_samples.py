from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ptdatabase import Powertool, Base, PowertoolItem, User

engine = create_engine('sqlite:///Powertool.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Yoon", email="ngyoon95@gmail.com.com",
             picture='https://scontent.fkul6-1.fna.fbcdn.net/v/t1.0-9/13445650_10207207495649264_2247837608154913258_n.jpg?_nc_eui2=v1%3AAeHxbggw7a7gzAjVKND4eZOMcdplkiAYMs634fupmSbctKVkAIPl7CS3zWVqATzMPYIbPF1Ztt4yzIEXBqWPQsss-gbhEcgezKoMZqbJy34DVQ&oh=dbb19d21f08c3c21d620a185ca28598a&oe=59CD56CE')
session.add(User1)
session.commit()

# Powertool for Bosch
Powertool1 = Powertool(user_id=1, brand="BOSCH")
session.add(Powertool1)
session.commit()

       
PowertoolItem1 = PowertoolItem(user_id=1, model="GWS13-50VS", description="Small angle grinders",
                     price="$50.99", category="Grinders", powertool=Powertool1)
session.add(PowertoolItem1)
session.commit()

PowertoolItem2 = PowertoolItem(user_id=1, model="1994-6/1994-6D", description="Large angle grinders",
                     price="$60.99", category="Grinders", powertool=Powertool1)
session.add(PowertoolItem2)
session.commit()

PowertoolItem3 = PowertoolItem(user_id=1, model="PS31", description="Cordless drill",
                     price="$103.99", category="Cordless Tools", powertool=Powertool1)
session.add(PowertoolItem3)
session.commit()

PowertoolItem4 = PowertoolItem(user_id=1, model="GP712VS", description="Die Grinders",
                     price="$67.99", category="Grinders", powertool=Powertool1)
session.add(PowertoolItem4)
session.commit()

PowertoolItem5 = PowertoolItem(user_id=1, model="CM10GD", description="10inch DUAL-BEVEL GLIDE MITER SAW",
                     price="$211.99", category="Woodworking", powertool=Powertool1)
session.add(PowertoolItem5)
session.commit()

PowertoolItem6 = PowertoolItem(user_id=1, model="GAM 220 MF", description="Digital angle finder and inclinometer",
                     price="$111.59", category="Measuring Tools", powertool=Powertool1)

session.add(PowertoolItem6)
session.commit()

PowertoolItem7 = PowertoolItem(user_id=1, model="D-TECT 150", description="Wall scanner with radar",
                    price="$3.49", category="Measuring Tools", powertool=Powertool1)
session.add(PowertoolItem7)
session.commit()

PowertoolItem8 = PowertoolItem(user_id=1, model="GLL 2-20", description="Self-Leveling, horizontal cross-line laser",
                     price="$315.59", category="Measuring Tools", powertool=Powertool1)
session.add(PowertoolItem8)
session.commit()
 



# Powertool for Makita
Powertool2 = Powertool(user_id=1, brand="MAKITA")
session.add(Powertool2)
session.commit()
       
PowertoolItem1 = PowertoolItem(user_id=1, model="XAG01", description="Cut-off angle grinder",
                     price="$40.99", category="Grinders", powertool=Powertool2)
session.add(PowertoolItem1)
session.commit()

PowertoolItem2 = PowertoolItem(user_id=1, model="GA5042C", description="Cordless 18V grinder",
                     price="$150.99", category="Cordless Tools", powertool=Powertool2)
session.add(PowertoolItem2)
session.commit()

PowertoolItem3 = PowertoolItem(user_id=1, model="GA7911", description="Angle sander",
                     price="$113.99", category="Grinders", powertool=Powertool2)
session.add(PowertoolItem3)
session.commit()

PowertoolItem4 = PowertoolItem(user_id=1, model="GD0801C", description="Die Grinders",
                     price="$67.99", category="Grinders", powertool=Powertool2)
session.add(PowertoolItem4)
session.commit()

PowertoolItem5 = PowertoolItem(user_id=1, model="LD080P", description="Range 262 feet",
                     price="$89.00", category="Measuring Tools", powertool=Powertool2)
session.add(PowertoolItem5)
session.commit()

PowertoolItem6 = PowertoolItem(user_id=1, model="SK103PZ", description="Self-Leveling, horizontal cross-line laser",
                     price="$325.00", category="Measuring Tools", powertool=Powertool2)
session.add(PowertoolItem6)
session.commit()

PowertoolItem7 = PowertoolItem(user_id=1, model="RP2301FC", description="3-1/4 HP* PLUNGE ROUTER",
                     price="$689.00", category="Woodworking", powertool=Powertool2)
session.add(PowertoolItem7)
session.commit()

PowertoolItem8 = PowertoolItem(user_id=1, model="BO6050J", description="6inch RANDOM ORBIT SANDER",
                     price="$65.50", category="Woodworking", powertool=Powertool2)
session.add(PowertoolItem8)
session.commit()



# Powertool for Hitachi
Powertool3 = Powertool(user_id=1, brand="HITACHI")
session.add(Powertool3)
session.commit()
       
PowertoolItem1 = PowertoolItem(user_id=1, model="G18DSL", description="Cordless angle grinder",
                     price="$140.99", category="Cordless Tools", powertool=Powertool3)
session.add(PowertoolItem1)
session.commit()

PowertoolItem2 = PowertoolItem(user_id=1, model="G23ST/CD", description="High power grinder",
                     price="$160.59", category="Grinders", powertool=Powertool3)
session.add(PowertoolItem2)
session.commit()

PowertoolItem3 = PowertoolItem(user_id=1, model="G23ST/CD", description="230mm angle grinder with Trigger switch",
                     price="$113.99", category="Grinders", powertool=Powertool3)
session.add(PowertoolItem3)
session.commit()

PowertoolItem4 = PowertoolItem(user_id=1, model="GP2S2", description="Die Grinders",
                     price="$37.99", category="Grinders", powertool=Powertool3)
session.add(PowertoolItem4)
session.commit()

PowertoolItem5 = PowertoolItem(user_id=1, model="C18DSL", description="18V Cordless Circular Saw",
                     price="$389.00", category="Cordless Tools", powertool=Powertool3)
session.add(PowertoolItem5)
session.commit()

PowertoolItem6 = PowertoolItem(user_id=1, model="CJ160V", description="160mm Jigsaw",
                     price="$85.00", category="Woodworking", powertool=Powertool3)
session.add(PowertoolItem6)
session.commit()

PowertoolItem7 = PowertoolItem(user_id=1, model="C8FSE", description="216mm Slide Compound Mitre Saw",
                     price="$1689.00", category="Woodworking", powertool=Powertool3)
session.add(PowertoolItem7)
session.commit()

PowertoolItem8 = PowertoolItem(user_id=1, model="SV12SG", description="110mm Orbital Sander",
                     price="$35.50", category="Woodworking", powertool=Powertool3)
session.add(PowertoolItem8)
session.commit()



# Powertool for Ryobi
Powertool4 = Powertool(user_id=1, brand="RYOBI")
session.add(Powertool4)
session.commit()
       
PowertoolItem1 = PowertoolItem(user_id=1, model="R18AG-0", description="18V Cordless Angle Grinder",
                     price="$240.99", category="Cordless Tools", powertool=Powertool4)
session.add(PowertoolItem1)
session.commit()

PowertoolItem2 = PowertoolItem(user_id=1, model="EAG2000RS", description="2000W Corded Angle Grinder, 230mm Disk",
                     price="$150.99", category="Grinders", powertool=Powertool4)
session.add(PowertoolItem2)
session.commit()

PowertoolItem3 = PowertoolItem(user_id=1, model="RAG600-115G", description="600W Corded Angle Grinder, 115mm disk",
                     price="$113.00", category="Grinders", powertool=Powertool4)
session.add(PowertoolItem3)
session.commit()

PowertoolItem4 = PowertoolItem(user_id=1, model="RJS720-G", description="500W Corded jigsaw",
                     price="$127.99", category="Woodworking", powertool=Powertool4)
session.add(PowertoolItem4)
session.commit()

PowertoolItem5 = PowertoolItem(user_id=1, model="EMS216L", description="1500W Corded Mitre Saw, 216m Blade",
                     price="$489.00", category="Woodworking", powertool=Powertool4)
session.add(PowertoolItem5)
session.commit()

PowertoolItem6 = PowertoolItem(user_id=1, model="EPS80RS", description="80W Corded Palm Sander",
                     price="$35.00", category="Woodworking", powertool=Powertool4)
session.add(PowertoolItem6)
session.commit()

PowertoolItem7 = PowertoolItem(user_id=1, model="RTS1800EF-G", description="1800W Corded Table Saw with Wheeled Stand",
                     price="$1489.00", category="Woodworking", powertool=Powertool4)
session.add(PowertoolItem7)
session.commit()

PowertoolItem8 = PowertoolItem(user_id=1, model="EHT150V", description="150W Corded Rotary Tool with 115 Accessories",
                     price="$45.00", category="Woodworking", powertool=Powertool4)
session.add(PowertoolItem8)
session.commit()

print "added menu items!"
