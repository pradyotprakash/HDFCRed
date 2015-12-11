import requests
from bs4 import BeautifulSoup

# headers = {
#     'User-Agent': 'meme',
#     'Accept': 'application/json, text/javascript, */*; q=0.01',
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
#     'X-Requested-With': 'XMLHttpRequest'
# }

headers = {
	'Accept':'*/*',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'en-US,en;q=0.8',
	'Connection':'keep-alive',
	'Content-Length':'1047',
	'Content-Type':'text/plain',
	'Cookie':'tvc_vid=21449045558212; mbUserUUID=aee31f51ea7a4c96be7c6578d4f25fa7FE97503911BCA4EF5AF3DF2A16E09284; affordEmiNetIncome=100000; affordEmiExistingLoan=; srpEmiTenure=20; srpEmiRoi=10; _mbRunstats=nu8egymu864w6zln; mf_abbdf9b5-e544-4446-a1d7-5f8999ab52f5=-1; _we_wk_ss_lsf_=true; 25201_LB_SHOWN=Y; _LB_SHOWN=Y; GDES=N; viewedProperties=17368757,18406973,18458096; repUser=id-18458096|th-S|bd-4|ct-Noida|lt-Sector_129|pr-Multistorey_Apartment|bg-1.1_Lac|id-18406973|th-S|bd-4|ct-Ahmedabad|lt-|category-S|r|pr-Villa|bg-1.0_Lac; detailsDynamicView=B; viewedPropertiesForDetails=17369382|18557250|18155361|18556313|18555331|18155711|17368757|16254203|18570028|18568497|18406973|18458096; contactTrackCookie=AC-RHS-Phone-B; lalec=1500000; rlec=10; ltlec=10; inlec=50000; ellec=10000; amountRequired=2500000; interestRate=10; loanTenureYear=10; larcc=2500000; rrcc=10; ltrcc=10; nrrcc=9; lsdrcc=2%2F12%2F2010; nrdrcc=2%2F12%2F2015; lalpc=2500000; rlpc=10; ltlpc=10; iplpc=40; palpc=100000; SHOWSEARCHTEXT=; __utmt=1; JSESSIONID=1556816EB251725882C0C0A4D3EBB51B-n1.MBAPP11; gaqCompleteCookie=sequenceNum=42||universalTimestamp=Fri Dec 04 2015 17:11:08 GMT+0530 (IST)||source=||sessionId=1556816EB251725882C0C0A4D3EBB51B-n1.MBAPP11||loginId=||homeSearchBuyRent=S||homeSearchTyped=||homeSearchCity=||homeSearchCityName=||homeSearchLocality=||homeSearchProject=||homeSearchLandmark=||homeSearchPropertyType=10002_10003_10021_10022,10001_10017||homeSearchBudgetMin=||homeSearchBudgetMax=||homeSearchbedrooms=||srpLandingPage=propertySearch||srpSearchType=1||srpcategory=S||srpCity=||srpCityName=||srpLocality=||srpProject=||srpLandmark=||srpPropertyType=10002_10003_10021_10022,10001_10017||srpBudgetMin=||srpBudgetMax=||srpbedrooms=||srpinputListings=||srpsaleType=||srppossessionYears=||srpageConstruction=||srpfurnished=||srpareaFrom=||srpareaTo=||srppostedSince=||srpamenities=||srpimageVideo=||srpverified=||srpdiscountsOffers=||srppropertiesIn=||srpOtherSortClick=||srpOtherPhotoClick=||srpOtherSuburbClick=||srpOtherShorstlistClick=||srpContactButtonClick=||srpContactDetailPageView=||srpContactPropertyId=||srpContactProjectName=||srpContactPsmId=||srpContactButtonOpenedSuccess=||srpContactPositionOfProperty=||srpContactBedroom=||srpContactPropertyType=||srpContactArea=||srpContactPrice=||srpContactNumberOfImages=||srpContactLocation=||srpContactDevName=||srpContactPostedBy=||srpContactRatePerSqft=||srpContactProjPropOrNot=||srpContactStatus=||srpContactTransaction=||srpContactFurnishingStatus=||srpContactFloorDetails=||srpContactBathrooms=||srpContactApprovals=||srpContactCommissionRate=||srpContactPostedDate=||srpContactVerified=||srpContactListingType=||srpContactCompletionScore=||srpContactIndexScore=||srpContactUserType=||srpDetailPageClickDetailPageView=||srpDetailPageClickPropertyId=||srpDetailPageClickProjectName=||srpDetailPageClickPsmId=||srpDetailPageClickPositionOfProperty=||srpDetailPageClickbedrooms=||srpDetailPageClickPropertyType=||srpDetailPageClickArea=||srpDetailPageClickPrice=||srpDetailPageClickNumberOfImages=||srpDetailPageClickLocation=||srpDetailPageClickDevName=||srpDetailPageClickPostedBy=||srpDetailPageClickRatePerSqft=||srpDetailPageClickProjPropOrNot=||srpDetailPageClickStatus=||srpDetailPageClickTransaction=||srpDetailPageClickFurnishingStatus=||srpDetailPageClickApprovals=||srpDetailPageClickCommissionRate=||srpDetailPageClickPostedDate=||srpDetailPageClickVerified=||srpDetailPageClickListingType=||srpDetailPageClickCompletionScore=||srpDetailPageClickIndexScore=||srpDetailPageClickUserType=||srpDetailPageLocality=||srpDetailPagePropertyType=||srpDetailPageBudget=||searchVersionAB=A; INT_PAGE=Y; _ga=GA1.2.930407449.1449045558; _gat=1; mbRecommendationCookies=pageType%3Dproperty%7ClistType%3DS%7CpropType%3D10002%2C10003%2C10021%2C10022%2C10001%2C10017%7CpageOption%3DA; defaultLeaderBoard=D; __utma=163479907.930407449.1449045558.1449224895.1449229268.11; __utmb=163479907.7.9.1449229272643; __utmc=163479907; __utmz=163479907.1449045558.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Nvis=78|1451637561916; _vz=viz_55c5d43929a43',
	'Host':'www.magicbricks.com',
	'Origin':'http://www.magicbricks.com',
	'Referer':'http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai-Metropolitan-Region&price=Y&pageOption=B',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'
}

s = requests.Session()

content = s.get('http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai-Metropolitan-Region&price=Y&pageOption=A')
open('out1','w').write(str(content.text))

content = s.get('http://www.magicbricks.com/bricks/ajax/updateSearchViews.json?pageNo=5', headers=headers)
open('out2','w').write(str(content.text))