#!/usr/bin/env python3
"""
Rewrite introductions of all Hugo articles with hook-driven, top-blogger style copy.
"""

import re
import os

# Map of filepath (relative from content/) -> new intro text
INTROS = {
    # ===== CULTURE =====
    "culture/dating-in-japan-foreigner.md": (
        "Most foreigners arrive in Japan with high hopes — and leave completely confused about dating here. "
        "The rules are different, the signals are subtle, and the cultural gap is real. "
        "This guide cuts through the mystery and gives you an honest picture of what dating in Japan actually looks like."
    ),
    "culture/emergency-guide-foreigners-japan.md": (
        "An earthquake at 2 a.m., a hospital visit where no one speaks English, a typhoon warning you can't read. "
        "Emergencies don't wait until you've learned the language. "
        "Here's the practical playbook every foreigner in Japan needs to have ready before anything goes wrong."
    ),
    "culture/gift-giving-japan-guide.md": (
        "You brought a gift — and somehow that made things awkward. "
        "Gift-giving in Japan follows an unwritten rulebook most foreigners never see. "
        "Get it right, and you build trust instantly. Get it wrong, and you may not even know why the mood shifted."
    ),
    "culture/golden-week-japan-guide.md": (
        "Golden Week looks like a dream on paper — a whole week off in Japan. "
        "In reality, bullet trains sell out in minutes, popular spots triple in price, and half the country is on the move at once. "
        "Here's how to navigate it without losing your mind or your budget."
    ),
    "culture/hanami-cherry-blossom-guide.md": (
        "Cherry blossom season lasts about two weeks. Miss the timing by a few days and it's gone for the year. "
        "Getting hanami right means knowing where to go, when to show up, and what to bring. "
        "This guide covers everything you need to make it memorable."
    ),
    "culture/how-to-use-trains-japan-foreigner.md": (
        "Japan's train network is the best in the world — and also one of the most confusing to figure out the first time. "
        "Wrong ticket, wrong line, wrong exit: it happens to everyone. "
        "Read this once and you'll navigate it like a local."
    ),
    "culture/izakaya-guide-foreigners.md": (
        "Walk into an izakaya without knowing the drill and you'll spend the evening nodding at things you don't understand. "
        "Walk in prepared and you'll have one of the best nights Japan has to offer. "
        "Here's exactly what to expect and how to order."
    ),
    "culture/japanese-drinking-culture-guide.md": (
        "Drinking in Japan isn't just about alcohol — it's how colleagues become friends and walls come down. "
        "Misread the room and you'll stand out for the wrong reasons. "
        "This guide explains the unwritten rules so you can enjoy nomikai without the awkwardness."
    ),
    "culture/japanese-etiquette-guide.md": (
        "Nobody expects you to be perfect — but a few missteps can leave a lasting impression you didn't intend. "
        "Japanese etiquette isn't complicated once you know the logic behind it. "
        "Here are the rules that actually matter in daily life."
    ),
    "culture/japanese-festivals-foreigners.md": (
        "Summer in Japan means festivals — and they're unlike anything you've experienced elsewhere. "
        "But showing up unprepared means missing the best parts. "
        "This guide tells you what to wear, what to eat, and how to actually enjoy matsuri season."
    ),
    "culture/japanese-food-etiquette.md": (
        "Stabbing your chopsticks upright in rice, pouring your own drink, leaving food on your plate — small habits that carry big meaning in Japan. "
        "Food is a social ritual here, and knowing the etiquette shows more respect than any Japanese phrase you'll learn. "
        "Here's what you need to know before your next meal."
    ),
    "culture/japanese-language-school-guide.md": (
        "Choosing the wrong Japanese language school is an expensive mistake that costs you months of progress. "
        "The right school can transform your Japanese — and your life in Japan. "
        "Here's how to evaluate your options and pick the one that actually fits your goals."
    ),
    "culture/japanese-neighborhood-etiquette.md": (
        "Your neighbors noticed everything on your first day. "
        "In Japan, how you behave in your building and on your street matters more than most foreigners realize. "
        "Get the basics right early and you'll avoid complaints, tension, and awkward confrontations."
    ),
    "culture/japanese-new-year-oshogatsu.md": (
        "New Year's in Japan is nothing like New Year's anywhere else. "
        "The streets go quiet, shrines fill up at midnight, and centuries-old traditions play out in ordinary neighborhoods. "
        "Here's how to experience Oshogatsu the way it's meant to be experienced."
    ),
    "culture/japanese-public-holidays-guide.md": (
        "Sixteen public holidays per year — and some of them cluster together in ways that shut down entire cities. "
        "Knowing Japan's holiday calendar isn't just convenient, it affects your schedule, your travel plans, and your work life. "
        "Here's a complete breakdown of every holiday and what it actually means day-to-day."
    ),
    "culture/jlpt-japanese-language-test.md": (
        "The JLPT can open doors in Japan — or just sit as a line on your resume that nobody asks about. "
        "Whether you're studying for career reasons or personal goals, knowing how the test actually works saves you wasted effort. "
        "Here's an honest guide to the JLPT from registration to results."
    ),
    "culture/language-exchange-japan.md": (
        "Language exchange sounds great in theory. In practice, you end up spending the whole session speaking English. "
        "Done right, language exchange is one of the fastest and cheapest ways to improve your Japanese — and meet real people. "
        "Here's how to make it work."
    ),
    "culture/making-friends-japan-foreigner.md": (
        "Many foreigners in Japan describe the same experience: polite colleagues, friendly conversations — but no real friends. "
        "Making genuine connections here takes a different approach than back home. "
        "This guide explains why, and what actually works."
    ),
    "culture/meishi-business-card-japan.md": (
        "You received a business card and shoved it in your back pocket. That was noticed. "
        "Meishi exchange is a ritual in Japan, and how you handle it in the first thirty seconds sets the tone for the entire relationship. "
        "Here's what to do — and what never to do."
    ),
    "culture/new-year-japan-guide.md": (
        "Japan transforms in the final days of December in a way you have to see to believe. "
        "Shops close, cities quiet down, and traditions that have lasted centuries play out on every street corner. "
        "Here's your complete guide to experiencing Japanese New Year like a local."
    ),
    "culture/sento-public-bath-japan.md": (
        "Walking into a sento for the first time without knowing the rules is a fast way to embarrass yourself and everyone around you. "
        "But sento culture is one of the most rewarding parts of life in Japan once you understand it. "
        "This guide covers everything — from what to bring to what never to do."
    ),
    "culture/shrine-temple-etiquette-japan.md": (
        "Shrines and temples are everywhere in Japan, and most foreigners walk through them without really knowing what they're looking at. "
        "A little context changes everything. "
        "Here's the etiquette and meaning behind Japan's most visited sacred spaces."
    ),
    "culture/workplace-culture-japan-foreigners.md": (
        "Japanese workplace culture can feel like a parallel universe if you're not prepared for it. "
        "Hierarchy, after-work drinks, unspoken rules about overtime — it all operates on a logic that takes time to decode. "
        "This guide gives you an honest picture of what to expect before your first day."
    ),

    # ===== DAILY LIFE =====
    "daily-life/arriving-japan-first-steps.md": (
        "The first month in Japan involves a specific sequence of administrative tasks — and doing them out of order wastes weeks. "
        "Most newcomers figure this out the hard way. "
        "This checklist lays out exactly what to do, in the right order, so you hit the ground running."
    ),
    "daily-life/best-apps-foreigners-japan.md": (
        "Living in Japan without the right apps means guessing your way through train changes, menus you can't read, and services that assume you speak Japanese. "
        "The right tools make daily life dramatically easier. "
        "Here are the apps that actually earn their place on your phone."
    ),
    "daily-life/best-cities-live-japan-foreigners.md": (
        "Choosing the wrong city is a mistake that takes a year to undo. "
        "Japan's major cities are more different from each other than most people expect — in cost, pace, foreigner infrastructure, and job market. "
        "Here's a clear-eyed comparison to help you decide where to actually land."
    ),
    "daily-life/best-neighborhoods-tokyo-foreigners.md": (
        "Tokyo is enormous, and your neighborhood shapes your entire life here — commute, community, cost, and comfort. "
        "Pick the wrong area and you'll spend two years wanting to move. "
        "Here's a neighborhood-by-neighborhood breakdown for foreigners figuring out where to live in Tokyo."
    ),
    "daily-life/best-sim-cards-for-foreigners-japan.md": (
        "Japan's mobile market is confusing if you don't know what you're looking for — and the most advertised plans aren't always the best deal for foreigners. "
        "The right SIM card can save you thousands of yen a month. "
        "Here's how to pick the one that actually fits your situation."
    ),
    "daily-life/best-vpn-for-foreigners-japan.md": (
        "Certain streaming services, banking apps, and news sites behave differently once you're in Japan. "
        "A VPN solves most of those problems — but not all VPNs work well here. "
        "Here's what you need to know before you subscribe."
    ),
    "daily-life/budget-travel-japan.md": (
        "Japan has a reputation for being expensive. It's partly deserved — and mostly misleading. "
        "Travel Japan the right way and you can eat brilliantly, sleep comfortably, and see the best of the country without spending a fortune. "
        "Here's exactly how to do it."
    ),
    "daily-life/buying-a-car-japan-foreigner.md": (
        "Buying a car in Japan as a foreigner involves paperwork, parking certificates, and rules that surprise most people. "
        "Get it wrong and the process stalls completely. "
        "This guide walks you through every step from finding the car to driving it home."
    ),
    "daily-life/car-insurance-japan-foreigner.md": (
        "Car insurance in Japan is mandatory — and the system works differently than in most countries. "
        "Without the right coverage, a single accident can be financially devastating. "
        "Here's everything you need to know before you get behind the wheel."
    ),
    "daily-life/cheap-grocery-shopping-japan.md": (
        "Groceries in Japan don't have to be expensive — if you know which stores to use, which products to buy, and when to shop. "
        "Most foreigners overpay for years simply because nobody told them the tricks locals use. "
        "Here's how to cut your food bill significantly."
    ),
    "daily-life/child-allowance-japan.md": (
        "Japan pays a monthly child allowance to parents — and many foreigners don't know they're entitled to claim it. "
        "The paperwork is manageable once you know what's required. "
        "Here's exactly how to apply and how much you can expect."
    ),
    "daily-life/childcare-nursery-japan-foreigner.md": (
        "Finding nursery care in Japan as a foreigner feels impossible at first — waitlists, paperwork in Japanese, an opaque points system. "
        "But parents who understand how the system works can navigate it far more successfully. "
        "Here's an honest guide to childcare in Japan for foreign families."
    ),
    "daily-life/children-healthcare-japan.md": (
        "Navigating healthcare for your child in a country where you don't speak the language fluently is stressful. "
        "Japan's children's healthcare system is actually excellent — once you know how to use it. "
        "Here's what every foreign parent in Japan needs to know."
    ),
    "daily-life/coin-laundry-japan-guide.md": (
        "Coin laundries in Japan are clean, cheap, and efficient — but the machines, signs, and etiquette are all in Japanese. "
        "First-time users waste money pressing the wrong buttons. "
        "Here's a clear walkthrough so you get it right from the start."
    ),
    "daily-life/convenience-stores-japan-guide.md": (
        "Japanese convenience stores are unlike anything you've used before. "
        "They're part grocery store, part bank, part government office, part restaurant — and open 24 hours a day. "
        "Here's everything a foreigner needs to know to get the most out of them."
    ),
    "daily-life/corporate-housing-shataku-japan.md": (
        "Some Japanese companies offer housing — called shataku — as part of the employment package, and it can save you enormous money. "
        "But the terms vary widely and not everyone knows to ask about it. "
        "Here's what shataku is, who qualifies, and whether it's worth taking."
    ),
    "daily-life/cycling-bike-japan-foreigners.md": (
        "A bicycle changes everything about daily life in Japan — shorter commutes, less crowded trains, lower costs. "
        "But there are rules, registration requirements, and parking laws most foreigners don't know about until they get a fine. "
        "Here's how to cycle in Japan the right way."
    ),
    "daily-life/cycling-japan-foreigner.md": (
        "Cycling in Japan is one of the great daily pleasures — until you get your bike impounded or fined for parking it in the wrong spot. "
        "The rules here are specific and enforced. "
        "This guide covers everything you need to ride freely and legally."
    ),
    "daily-life/drivers-license-japan-foreigner.md": (
        "Getting a Japanese driver's license as a foreigner takes anywhere from one afternoon to several weeks — depending entirely on which country issued your current license. "
        "Knowing which path applies to you saves enormous time and money. "
        "Here's how the process works for each country."
    ),
    "daily-life/driving-in-japan-foreigner.md": (
        "Japan drives on the left, the road signs mix Japanese and symbols, and the rules around parking are stricter than most foreigners expect. "
        "Drive unprepared and you'll face fines, confusion, or worse. "
        "This guide covers the practical essentials for foreigners getting behind the wheel in Japan."
    ),
    "daily-life/earthquake-preparedness-japan.md": (
        "Japan averages 1,500 earthquakes a year. Most are minor — but the big ones happen without warning. "
        "Having a plan before disaster strikes is the difference between managing it and being helpless. "
        "Here's what every foreigner living in Japan should have prepared right now."
    ),
    "daily-life/garbage-sorting-recycling-japan.md": (
        "Putting out the garbage wrong in Japan isn't just embarrassing — it can result in your bags being rejected and left on the street with a note attached. "
        "Garbage sorting here is detailed and varies by municipality. "
        "Here's how to get it right without spending a week deciphering Japanese rules."
    ),
    "daily-life/grocery-delivery-japan.md": (
        "Japan's grocery delivery landscape has expanded dramatically — but the best services differ by city, language support, and what you're actually trying to buy. "
        "Some are foreigner-friendly, some are a frustrating ordeal without Japanese skills. "
        "Here's a practical breakdown of the options worth your time."
    ),
    "daily-life/gym-fitness-japan-foreigner.md": (
        "Finding a gym in Japan that fits your budget, location, and English comfort level takes more research than it should. "
        "Some chains are genuinely foreigner-friendly; others have sign-up processes that will test your patience. "
        "Here's a clear comparison of your best options."
    ),
    "daily-life/home-internet-wifi-japan.md": (
        "Home internet in Japan is fast — genuinely among the fastest in the world. "
        "But setting it up as a foreigner involves navigating Japanese-language contracts, installation windows, and router fees. "
        "Here's how to get connected quickly without overpaying."
    ),
    "daily-life/hospital-clinic-japan-foreigner.md": (
        "Walking into a Japanese hospital without a plan is a disorienting experience — different departments, different paperwork, and a system built entirely in Japanese. "
        "Knowing how it works in advance takes most of the stress out of it. "
        "Here's a practical guide to using hospitals and clinics in Japan as a foreigner."
    ),
    "daily-life/housing-costs-japan-cities.md": (
        "Housing costs in Japan vary dramatically by city — and the gap is larger than most people moving here expect. "
        "Where you choose to live affects your entire financial picture. "
        "Here's an honest, current comparison of rental costs across Japan's major cities."
    ),
    "daily-life/how-to-open-bank-account-japan-foreigner.md": (
        "Opening a bank account in Japan as a new foreigner used to be nearly impossible. "
        "It's gotten easier — but the requirements still trip people up if they don't know what to bring. "
        "Here's exactly what you need and which banks are most foreigner-friendly."
    ),
    "daily-life/how-to-rent-apartment-japan-foreigner.md": (
        "Renting an apartment in Japan as a foreigner involves a set of hurdles you won't find in most countries — guarantors, key money, and landlords who may decline foreigners outright. "
        "Knowing how the system works gives you a real advantage. "
        "Here's a step-by-step guide to renting in Japan successfully."
    ),
    "daily-life/how-to-set-up-utilities-japan.md": (
        "Setting up electricity, gas, and water in Japan sounds straightforward — until you realize the process involves phone calls or web forms that are entirely in Japanese. "
        "Most foreigners rely on a helpful colleague or neighbor. "
        "This guide lets you handle it yourself."
    ),
    "daily-life/international-schools-japan.md": (
        "International school fees in Japan are significant — often ¥2 million or more per year. "
        "But not all international schools are equal, and the right fit depends on curriculum, language, and your family's plans. "
        "Here's what to evaluate before making one of the biggest education decisions of your time in Japan."
    ),
    "daily-life/japan-post-guide-foreigners.md": (
        "Japan Post does a lot more than deliver letters. "
        "It handles banking, insurance, and package services that foreigners use constantly — once they know how. "
        "Here's a foreigner's guide to getting the most out of Japan Post."
    ),
    "daily-life/japan-post-office-guide.md": (
        "The post office in Japan is quietly one of the most useful institutions a foreigner can access. "
        "Banking, savings, package pickup, and international shipping all under one roof. "
        "Here's everything you need to use it effectively."
    ),
    "daily-life/japan-public-holidays.md": (
        "Japan has sixteen public holidays, and several cluster together in ways that affect everything from business schedules to travel costs. "
        "Miss the pattern and you'll be caught off-guard repeatedly. "
        "Here's the complete calendar with context for what each holiday actually means."
    ),
    "daily-life/japan-school-system-guide.md": (
        "Japan's school system is structured differently from most Western countries, and foreign parents often find themselves unprepared for how it works. "
        "From enrollment to daily routines to the exam culture, the differences are significant. "
        "Here's a clear guide for families navigating Japanese schools."
    ),
    "daily-life/japan-summer-survival-guide.md": (
        "Japanese summer is genuinely brutal — not just hot, but oppressively humid in a way that shocks people who thought they knew heat. "
        "The good news is that locals have developed the tools and habits to handle it. "
        "Here's how to survive — and even enjoy — summer in Japan."
    ),
    "daily-life/japan-winter-guide.md": (
        "Winter in Japan catches many foreigners off guard — not because of the cold itself, but because Japanese apartments are often poorly insulated and the heating systems work differently than expected. "
        "Knowing what to prepare for makes a huge difference. "
        "Here's how to stay warm and comfortable through the Japanese winter."
    ),
    "daily-life/japanese-apartment-rules.md": (
        "Japanese apartments come with a detailed set of rules — some written into your contract, some just understood. "
        "Break them unknowingly and you risk losing your deposit or your lease. "
        "Here's what the rules actually cover and how to stay on the right side of them."
    ),
    "daily-life/japanese-apartment-types.md": (
        "1K, 1LDK, 2DK — Japanese apartment listings use shorthand that leaves most foreigners baffled. "
        "Once you crack the code, comparing apartments becomes much faster. "
        "Here's a plain-English breakdown of every apartment type you'll encounter."
    ),
    "daily-life/japanese-customs-immigration-guide.md": (
        "Arriving in Japan goes smoothly when you know what to expect at customs and immigration. "
        "It goes badly when you don't. "
        "Here's a clear walkthrough of the entire arrival process so there are no surprises."
    ),
    "daily-life/japanese-emergency-services.md": (
        "In an emergency, the last thing you want to be doing is searching for phone numbers. "
        "Japan's emergency services work well — but they operate in Japanese, and the system has quirks foreigners often don't know about. "
        "Bookmark this before you need it."
    ),
    "daily-life/japanese-hanko-seal-guide.md": (
        "You'll encounter hanko within your first week in Japan — on rental contracts, bank forms, and official documents. "
        "Many foreigners don't realize they need one until they're standing at a counter unable to proceed. "
        "Here's what hanko is, when you need it, and how to get one."
    ),
    "daily-life/japanese-public-transport-guide.md": (
        "Japan's public transport network is the most efficient in the world — but it has a learning curve that most newcomers underestimate. "
        "IC cards, express lines, reserved seats, last trains — get these wrong and you'll end up stranded or overcharged. "
        "Here's how to use it like someone who's been here for years."
    ),
    "daily-life/japanese-supermarket-guide.md": (
        "Japanese supermarkets are organized differently, labeled differently, and stocked with products you won't recognize at first. "
        "That's half the fun — but also the source of some expensive mistakes. "
        "Here's a guide to navigating Japanese supermarkets with confidence from day one."
    ),
    "daily-life/jp-bank-japan-post-bank.md": (
        "Japan Post Bank — JP Bank — is one of the easiest bank accounts for foreigners to open in Japan. "
        "No complex requirements, nationwide ATM access, and international transfers supported. "
        "Here's everything you need to know to open and use an account."
    ),
    "daily-life/jr-pass-guide-foreigners-japan.md": (
        "The JR Pass costs a significant amount of money. Whether it actually saves you money depends entirely on how you use it. "
        "Many tourists buy it by default and end up overpaying. "
        "Here's the honest math — and when it's actually worth it."
    ),
    "daily-life/karaoke-japan-foreigners.md": (
        "Karaoke in Japan is not the public humiliation most Westerners imagine — it's private rooms, cheap drinks, and one of the most fun social experiences the country offers. "
        "First-timers are always surprised. "
        "Here's how to enjoy it from the moment you walk in."
    ),
    "daily-life/learning-japanese-best-resources.md": (
        "Most people start learning Japanese with enthusiasm and stall out within three months. "
        "The problem is almost always resources and method, not ability. "
        "Here are the tools that actually produce results — ranked honestly by what works best at each stage."
    ),
    "daily-life/learning-japanese-resources.md": (
        "Learning Japanese is hard. Choosing the wrong resources makes it much harder. "
        "After years of living in Japan and watching what actually works, some patterns become clear. "
        "Here's a practical guide to the resources worth your time."
    ),
    "daily-life/living-fukuoka-as-foreigner.md": (
        "Fukuoka keeps appearing on lists of the best cities to live in Asia — and for foreigners, it often outperforms expectations. "
        "Cheap, relaxed, connected to the rest of Japan, and easier to navigate than Tokyo. "
        "Here's an honest look at what life in Fukuoka is actually like."
    ),
    "daily-life/living-kyoto-as-foreigner.md": (
        "Living in Kyoto is different from visiting Kyoto. "
        "The charm is real, but so are the tourist crowds, the housing competition, and the deeply traditional community culture. "
        "Here's what daily life in Kyoto actually looks like for a foreign resident."
    ),
    "daily-life/living-nagoya-as-foreigner.md": (
        "Nagoya is one of Japan's most underrated cities — a major economic hub that most expats overlook in favor of Tokyo or Osaka. "
        "Lower costs, less competition, strong manufacturing and automotive industries. "
        "Here's what living in Nagoya as a foreigner is really like."
    ),
    "daily-life/living-osaka-as-foreigner.md": (
        "Osaka has a reputation for being louder, friendlier, and more affordable than Tokyo — and it earns that reputation. "
        "But the reality of living here as a foreigner has its own quirks and challenges. "
        "Here's an honest guide to daily life in Osaka."
    ),
    "daily-life/living-sapporo-as-foreigner.md": (
        "Sapporo sits in a different climate zone from most of Japan — winters are serious, summers are genuinely comfortable, and the pace of life is slower. "
        "For foreigners who want Japan without the Tokyo intensity, it's worth a closer look. "
        "Here's what living in Sapporo is actually like."
    ),
    "daily-life/living-tokyo-as-foreigner.md": (
        "Tokyo is where most foreigners land, and most of them never really figure it out — they live in it without understanding it. "
        "The city rewards people who take the time to learn how it works. "
        "Here's a practical guide to actually living in Tokyo, not just surviving it."
    ),
    "daily-life/luggage-storage-shipping-japan.md": (
        "Traveling between cities in Japan with heavy luggage is entirely optional — Japan's luggage forwarding system is fast, cheap, and incredibly reliable. "
        "Most foreigners don't know it exists until someone shows them. "
        "Here's how to use it."
    ),
    "daily-life/moving-to-japan-checklist.md": (
        "Moving to Japan involves dozens of tasks that need to happen in a specific order — get the sequence wrong and you're waiting weeks for things that should take days. "
        "This checklist covers every step from before departure to your first month on the ground."
    ),
    "daily-life/moving-within-japan.md": (
        "Moving apartments within Japan involves more paperwork and more money than most people expect — key money, re-registration, utility transfers, and more. "
        "Knowing the process in advance saves real money and avoids nasty surprises. "
        "Here's a complete walkthrough."
    ),
    "daily-life/online-shopping-japan-foreigners.md": (
        "Japan's online shopping ecosystem is excellent — but much of it operates in Japanese, and not all platforms are foreigner-friendly. "
        "The right platforms save you enormous time and money. "
        "Here's a guide to shopping online in Japan as a foreign resident."
    ),
    "daily-life/onsen-guide-foreigners-japan.md": (
        "Onsen is one of the best things about living in Japan — but first-timers often approach it with anxiety they don't need to have. "
        "The etiquette is simple. The experience is worth it. "
        "Here's everything you need to enjoy onsen with confidence."
    ),
    "daily-life/package-delivery-japan.md": (
        "Japan's package delivery system is world-class — precise delivery windows, easy redelivery, and multiple pickup options. "
        "But the notes left on your door and the automated phone systems are in Japanese. "
        "Here's how to handle deliveries without missing your packages."
    ),
    "daily-life/pet-ownership-japan-foreigner.md": (
        "Bringing a pet to Japan or getting one here involves regulations, costs, and apartment rules that catch many foreigners off guard. "
        "Done right, it's entirely manageable. "
        "Here's the full picture on pet ownership in Japan."
    ),
    "daily-life/pocket-wifi-mobile-internet-japan.md": (
        "Pocket WiFi and SIM cards are both solid options for staying connected in Japan — but which one makes sense depends entirely on your situation. "
        "Choosing the wrong option means either overpaying or dealing with constant connectivity problems. "
        "Here's how to decide."
    ),
    "daily-life/renting-apartment-japan-foreigner.md": (
        "Japan's rental market has some of the most unique requirements in the world — guarantors, agency fees, key money, and landlords who sometimes decline foreign applicants. "
        "Understanding the system gives you a real edge. "
        "Here's a practical guide to renting in Japan as a foreigner."
    ),
    "daily-life/second-hand-shopping-japan.md": (
        "Japan's second-hand market is enormous, affordable, and full of items in near-perfect condition — because Japanese people take exceptional care of their possessions. "
        "Foreigners who discover it early save thousands. "
        "Here's where to shop and what to look for."
    ),
    "daily-life/sending-money-overseas-japan.md": (
        "Sending money overseas from Japan is something most foreigners do regularly — and most of them are overpaying on fees and exchange rates. "
        "The best services for international transfers from Japan can save you significant money each year. "
        "Here's how to compare your options."
    ),
    "daily-life/social-insurance-japan-foreigners.md": (
        "Social insurance in Japan isn't optional — it's mandatory, and your employer or local ward office will expect you to be enrolled. "
        "Many foreigners arrive without understanding how the system works or what they're paying into. "
        "Here's a clear explanation of what social insurance covers and what it costs."
    ),
    "daily-life/suica-ic-card-guide-japan.md": (
        "Suica is the single most useful thing you can set up on your first day in Japan. "
        "One card handles trains, buses, convenience stores, and vending machines across the country. "
        "Here's how to get one, load it, and use it everywhere."
    ),
    "daily-life/typhoon-preparedness-japan.md": (
        "Japan's typhoon season runs from summer through early autumn, and the storms can be severe enough to shut down cities entirely. "
        "Preparation before a typhoon arrives is what keeps it manageable. "
        "Here's what every foreigner in Japan should have ready before the season starts."
    ),
    "daily-life/what-is-my-number-card-japan.md": (
        "My Number is Japan's national identification system, and if you live in Japan, you have one whether you've used it or not. "
        "The physical card unlocks a growing range of services that make life significantly easier. "
        "Here's what it is, how to get the card, and when you'll actually need it."
    ),

    # ===== HEALTH =====
    "health/best-private-health-insurance-foreigners-japan.md": (
        "Japan's national health insurance is good — but it doesn't cover everything, and for foreigners with specific needs, the gaps matter. "
        "Private health insurance can fill those gaps, but the options vary enormously in coverage and value. "
        "Here's how to evaluate what you actually need."
    ),
    "health/dental-care-japan-foreigner.md": (
        "Dental care in Japan is affordable, technically excellent, and widely available — but the system works differently than most foreigners expect. "
        "Knowing how to navigate it saves money and avoids confusion. "
        "Here's a practical guide to dental care in Japan."
    ),
    "health/dentist-japan-foreigner.md": (
        "Finding a good dentist in Japan as a foreigner is easier than it sounds — but it does require knowing what to look for. "
        "English-speaking dentists exist in most major cities, and national health insurance covers more than most people realize. "
        "Here's how to get good dental care in Japan."
    ),
    "health/eye-care-optician-japan.md": (
        "Eye care in Japan is fast, affordable, and technically impressive — glasses are often ready in an hour and contact lenses are widely available. "
        "But the system has some quirks that foreigners consistently find surprising. "
        "Here's what you need to know."
    ),
    "health/hay-fever-pollen-japan.md": (
        "Japan's spring pollen season is one of the worst in the world, and it affects up to 40% of the population. "
        "Many foreigners arrive with no history of allergies and develop symptoms within their first spring here. "
        "Here's how to manage it."
    ),
    "health/how-japanese-health-insurance-works-foreigners.md": (
        "Japan's health insurance system is comprehensive and mandatory — and yet most foreigners who arrive here don't fully understand how it works until they need it. "
        "Knowing the system in advance means fewer surprises at the clinic. "
        "Here's how it actually works."
    ),
    "health/how-to-see-a-doctor-japan-foreigner.md": (
        "Seeing a doctor in Japan for the first time as a foreigner is less complicated than it seems — but only if you know how the system works. "
        "Walking in unprepared means confusion, delays, and sometimes the wrong treatment. "
        "Here's a practical guide to navigating Japanese healthcare."
    ),
    "health/japanese-health-checkup-guide.md": (
        "Annual health checkups in Japan are standardized, efficient, and often subsidized by your employer or local government. "
        "Most foreigners either skip them or don't know they're entitled to them. "
        "Here's what the checkup covers and how to access it."
    ),
    "health/mental-health-japan-foreigner.md": (
        "Mental health support for foreigners in Japan is available — but it's not always easy to find, and the cultural approach to mental health here is different from what many Westerners are used to. "
        "Knowing your options before you need them is the most important thing. "
        "Here's a practical guide to mental health resources in Japan."
    ),
    "health/mental-health-support-japan.md": (
        "Living abroad is harder on mental health than most people admit before moving. "
        "Japan has its own particular pressures — isolation, language barriers, work culture — and support services exist if you know where to look. "
        "Here's an honest guide to mental health resources in Japan."
    ),
    "health/pharmacy-medicine-japan.md": (
        "Japanese pharmacies are well-stocked and easy to use — but the medications available over the counter differ from what you might find at home, and some common drugs are simply not available here. "
        "Knowing the system saves time when you're sick and need help fast. "
        "Here's how Japanese pharmacies work."
    ),
    "health/pregnancy-childbirth-japan-foreigner.md": (
        "Having a baby in Japan as a foreigner is entirely manageable — but the system has its own structure, paperwork, and expectations that differ significantly from Western healthcare. "
        "Getting familiar with the process early reduces stress enormously. "
        "Here's what to expect from pregnancy through childbirth in Japan."
    ),

    # ===== JOBS =====
    "jobs/best-job-sites-for-foreigners-japan.md": (
        "Most foreigners job-hunting in Japan start with Google and end up on the wrong platforms. "
        "The best job sites for foreigners are specific, and the ones worth your time vary by industry and language ability. "
        "Here's a direct comparison of where to actually find jobs in Japan."
    ),
    "jobs/career-advancement-japan-foreigner.md": (
        "Getting promoted in a Japanese company as a foreigner requires understanding rules that aren't written anywhere. "
        "The path forward looks different here than in most Western workplaces. "
        "Here's what career advancement actually looks like for foreigners in Japan — and how to position yourself for it."
    ),
    "jobs/engineer-visa-japan-guide.md": (
        "The Engineer/Specialist in Humanities/International Services visa covers the widest range of skilled work in Japan — IT, engineering, business, and more. "
        "Getting it wrong costs months. Getting it right opens the door to working legally in Japan with a legitimate employer. "
        "Here's the complete guide."
    ),
    "jobs/freelance-self-employed-japan.md": (
        "Going freelance in Japan as a foreigner is possible — but it involves visa restrictions, tax registration, and business banking hurdles that most people don't anticipate. "
        "Understanding the rules before you start saves significant headaches. "
        "Here's what you need to know."
    ),
    "jobs/freelancing-in-japan-foreigner.md": (
        "Freelancing in Japan looks attractive — flexible work, your own clients, no office politics. "
        "The reality involves navigating visa requirements, client expectations, and a tax system built for salaried employees. "
        "Here's an honest guide to making it work."
    ),
    "jobs/how-to-change-jobs-with-work-visa-japan.md": (
        "Changing jobs in Japan on a work visa isn't always straightforward — your visa may be tied to your current employer in ways that create real constraints. "
        "Knowing the rules before you resign protects your legal status. "
        "Here's exactly how job changes work on a Japanese work visa."
    ),
    "jobs/it-jobs-foreigners-japan.md": (
        "Japan's tech industry has a genuine shortage of skilled engineers — and that shortage creates real opportunity for foreign IT professionals. "
        "But the market works differently than in the US or Europe. "
        "Here's a practical guide to finding and landing IT jobs in Japan."
    ),
    "jobs/japan-company-benefits-foreigners.md": (
        "Japanese companies offer a range of benefits that many foreign employees don't fully understand or claim. "
        "From commuting allowances to housing subsidies, knowing what to negotiate for makes a significant difference to your overall package. "
        "Here's what's typically on the table."
    ),
    "jobs/japanese-job-interview-guide.md": (
        "A Japanese job interview follows conventions that most foreigners haven't encountered before — formal structure, specific questions, and expectations around presentation that differ from Western norms. "
        "Prepare for the right things and you'll stand out. "
        "Here's exactly what to expect."
    ),
    "jobs/japanese-rirekisho-guide.md": (
        "The rirekisho is Japan's traditional resume format — handwritten, formatted, and unlike anything you've submitted before. "
        "Getting it wrong signals lack of attention to detail before you've even had an interview. "
        "Here's how to complete one properly."
    ),
    "jobs/japanese-vs-foreign-companies.md": (
        "Working at a Japanese company versus a foreign company in Japan are two genuinely different experiences — in culture, hours, hierarchy, and career trajectory. "
        "Neither is universally better. The right choice depends on your goals and tolerance for certain trade-offs. "
        "Here's an honest comparison."
    ),
    "jobs/job-hunting-japan-foreigner.md": (
        "Job hunting in Japan as a foreigner is not like job hunting anywhere else. "
        "The market has real demand for foreign talent — but you need to know where to look and how to present yourself. "
        "Here's a practical guide to finding work in Japan."
    ),
    "jobs/linkedin-job-search-japan.md": (
        "LinkedIn works in Japan — but it works differently here than in most Western countries, and using it the wrong way means getting no response from recruiters. "
        "A few adjustments to your approach can dramatically improve your results. "
        "Here's how to use LinkedIn effectively for job searching in Japan."
    ),
    "jobs/part-time-work-foreigners-japan.md": (
        "Part-time work in Japan as a foreigner is legally possible on most visa types — but the rules on hours and job types depend on your specific visa status. "
        "Getting this wrong has serious immigration consequences. "
        "Here's what you're actually allowed to do and how to find work."
    ),
    "jobs/remote-work-japan-foreigner.md": (
        "Remote work and Japan have a complicated relationship — visa rules, tax implications, and cultural expectations around physical presence all create friction that most remote workers don't anticipate. "
        "Here's what you actually need to know before working remotely from Japan."
    ),
    "jobs/salary-negotiation-japan.md": (
        "Salary negotiation in Japan is unusual — many companies present offers as fixed, and pushing back can feel culturally awkward. "
        "But negotiation is possible, and knowing how to approach it makes a real difference to your starting package. "
        "Here's how to negotiate salary effectively in the Japanese context."
    ),
    "jobs/shukkatsu-guide-japan-foreigner.md": (
        "Shukkatsu — Japan's new graduate job hunting season — operates on a calendar and process that shocks most foreigners encountering it for the first time. "
        "It is highly structured, starts earlier than you'd expect, and has its own rituals and expectations. "
        "Here's how to navigate it as a foreign student or graduate."
    ),
    "jobs/teaching-english-japan-guide.md": (
        "Teaching English in Japan remains one of the most accessible paths to living and working here legally — but the experience varies enormously depending on where and how you do it. "
        "ALT programs, eikaiwa schools, and private tutoring are completely different worlds. "
        "Here's how to choose the right path."
    ),
    "jobs/teaching-english-japan.md": (
        "Japan hires thousands of English teachers every year — and the demand shows no sign of slowing. "
        "But not all English teaching jobs are created equal, and signing the wrong contract is a year-long mistake. "
        "Here's what you need to know before applying."
    ),
    "jobs/visa-sponsorship-japan.md": (
        "Visa sponsorship is the gateway to working legally in Japan — and finding employers willing to sponsor is the challenge most foreign job seekers underestimate. "
        "The right approach, the right industries, and the right platforms make it achievable. "
        "Here's how to find visa-sponsoring employers in Japan."
    ),
    "jobs/working-japan-without-japanese.md": (
        "Working in Japan without speaking Japanese is possible — but the path is narrower than most people think, and the industries where it works are specific. "
        "Knowing where your skills fit opens real opportunities. "
        "Here's an honest guide to working in Japan without Japanese language ability."
    ),
    "jobs/working-overtime-japan.md": (
        "Overtime in Japan has a reputation — some of it deserved, much of it exaggerated. "
        "But the culture around hours worked, karoshi, and work-life balance is real and affects foreign employees in specific ways. "
        "Here's what to expect and how to navigate it."
    ),

    # ===== MONEY =====
    "money/atm-guide-foreigners-japan.md": (
        "Japan is still a cash-heavy country, and finding an ATM that actually accepts your foreign card is not as simple as it sounds. "
        "The wrong ATM will decline you at the most inconvenient moment. "
        "Here's exactly which ATMs work for foreigners and how to use them."
    ),
    "money/best-money-transfer-apps-from-japan.md": (
        "Sending money from Japan to your home country costs more than it should if you're using the wrong service. "
        "The best money transfer apps can save you thousands of yen per transaction. "
        "Here's a direct comparison of what's available from Japan."
    ),
    "money/buying-property-japan-foreigner.md": (
        "Foreigners can buy property in Japan with almost no legal restrictions — which surprises most people. "
        "The process is manageable, the prices are often lower than comparable Western cities, and Japan property can be a genuine opportunity. "
        "Here's how the buying process works."
    ),
    "money/cashless-payments-japan.md": (
        "Japan's cashless payment landscape is fragmented — IC cards, QR codes, credit cards, and convenience store apps all coexist with a society that still reaches for cash by default. "
        "Knowing which systems to use where saves time and gets you the best deals. "
        "Here's how to navigate it."
    ),
    "money/consumption-tax-refund-japan.md": (
        "Foreign visitors to Japan can claim consumption tax refunds on qualifying purchases — and the amounts add up quickly on major purchases. "
        "Most tourists don't claim everything they're entitled to because they don't know the rules. "
        "Here's how to do it correctly."
    ),
    "money/cost-of-living-japan-2025.md": (
        "Japan's cost of living reputation is outdated. The yen's weakness has made Japan more affordable than most Western countries for many categories of spending — and more expensive in others. "
        "Here's a current, honest breakdown of what life actually costs in Japan in 2025."
    ),
    "money/credit-card-guide-foreigners-japan.md": (
        "Using the wrong credit card in Japan costs you money on every transaction — foreign transaction fees, poor exchange rates, and missed rewards. "
        "The right card setup for Japan is different from what works at home. "
        "Here's what to use and what to avoid."
    ),
    "money/crypto-japan-foreigners.md": (
        "Japan is one of the most regulated crypto markets in the world — and for foreigners who want to invest in crypto while living here, the rules create specific constraints. "
        "Knowing the legal landscape protects you. "
        "Here's how crypto works for foreign residents in Japan."
    ),
    "money/currency-exchange-japan.md": (
        "Currency exchange rates in Japan vary dramatically by location — airports are the worst, post offices and some convenience stores are among the best. "
        "Where you exchange money is a decision worth thinking about. "
        "Here's how to get the best rate in Japan."
    ),
    "money/earthquake-insurance-japan.md": (
        "Standard apartment insurance in Japan does not cover earthquake damage — that requires a separate earthquake insurance policy. "
        "Given Japan's seismic activity, this is not a gap worth leaving open. "
        "Here's how earthquake insurance works and whether you need it."
    ),
    "money/filing-taxes-japan-foreigner.md": (
        "Tax filing in Japan is mandatory for most foreigners earning income here — and failing to file, or filing incorrectly, creates problems that are hard to resolve later. "
        "The process is more straightforward than it seems once you understand the structure. "
        "Here's a complete guide to filing taxes in Japan as a foreigner."
    ),
    "money/freelance-tax-japan.md": (
        "Freelance taxes in Japan catch most self-employed foreigners off guard. "
        "The rules on what you owe, when to pay, and how to register as a business are specific — and the penalties for getting it wrong are real. "
        "Here's what every freelancer in Japan needs to know."
    ),
    "money/furusato-nozei-guide-foreigners.md": (
        "Furusato Nozei — hometown tax — is one of Japan's best-kept money-saving secrets, and most foreigners who pay residence tax here have no idea they're eligible. "
        "Done right, you can receive thousands of yen in local goods and products at essentially no net cost. "
        "Here's how it works."
    ),
    "money/home-renters-insurance-japan.md": (
        "Renters insurance in Japan is cheap, often required by landlords, and covers more than most tenants realize. "
        "Skipping it is a false economy. "
        "Here's what renters insurance covers in Japan and how to get the right policy."
    ),
    "money/how-to-file-taxes-japan-foreigner.md": (
        "Filing a tax return in Japan for the first time feels overwhelming — the forms are in Japanese, the rules are specific, and the deadlines are unforgiving. "
        "Once you understand the structure, it's actually manageable. "
        "Here's a step-by-step guide to filing taxes in Japan as a foreign resident."
    ),
    "money/inheritance-tax-japan-foreigner.md": (
        "Japan's inheritance tax is one of the highest in the world, and it can apply to foreign residents in ways that most people don't anticipate until it's too late. "
        "Understanding your exposure is critical if you have significant assets or family overseas. "
        "Here's how inheritance tax works for foreigners in Japan."
    ),
    "money/investing-japan-foreigner-guide.md": (
        "Investing while living in Japan as a foreigner involves tax implications, account restrictions, and platform choices that don't apply to Japanese residents. "
        "Getting the setup right from the beginning saves significant complications later. "
        "Here's a practical guide to investing in Japan as a foreign resident."
    ),
    "money/japan-salary-guide-foreigners.md": (
        "Salary expectations in Japan are often misaligned for foreigners coming from Western markets — in some sectors higher, in many lower, and structured differently across the board. "
        "Knowing the actual numbers puts you in a better position to negotiate. "
        "Here's a realistic salary guide for foreigners working in Japan."
    ),
    "money/japan-travel-insurance-residents.md": (
        "Japan's national health insurance covers you domestically — but the moment you leave the country, you're uninsured unless you have separate travel coverage. "
        "For residents who travel regularly, the right travel insurance policy matters. "
        "Here's how to choose one."
    ),
    "money/japanese-credit-cards-foreigners.md": (
        "Getting a Japanese credit card as a foreigner is harder than it should be — most domestic cards require a credit history in Japan that takes years to build. "
        "But options exist, and the right card unlocks significant discounts and rewards. "
        "Here's how to get one and which cards are actually attainable."
    ),
    "money/life-insurance-japan-foreigner.md": (
        "Life insurance in Japan is widely available, competitively priced, and accessible to foreign residents — but the range of products is bewildering. "
        "Understanding what you actually need simplifies the decision significantly. "
        "Here's a practical guide to life insurance in Japan for foreigners."
    ),
    "money/national-pension-japan-foreigners.md": (
        "Japan's national pension system is mandatory for most foreign residents — and many foreigners are either unaware they're enrolled or unsure whether contributions are worth making. "
        "The good news: there's a refund program when you leave. "
        "Here's everything you need to know."
    ),
    "money/nisa-account-japan-guide.md": (
        "NISA is Japan's tax-free investment account — similar in concept to an ISA or Roth IRA — and foreign residents can open one. "
        "Most foreigners never use it because they don't know they're eligible. "
        "Here's how NISA works and whether it makes sense for you."
    ),
    "money/nisa-investing-japan-foreigner.md": (
        "NISA allows foreign residents in Japan to invest tax-free — but most foreigners don't know they qualify or how to actually open an account. "
        "The 2024 NISA reform made it significantly more powerful. "
        "Here's a clear guide to using NISA as a foreigner."
    ),
    "money/pension-lump-sum-refund-japan.md": (
        "When you leave Japan, you may be able to claim a lump-sum refund of the pension contributions you paid — and the window to claim it is short. "
        "Thousands of foreigners leave without claiming money they're entitled to. "
        "Here's how the pension refund works and how to apply."
    ),
    "money/rakuten-ecosystem-foreigners-japan.md": (
        "Rakuten's ecosystem of apps and services can save foreigners in Japan significant money — if you understand how the points system actually works. "
        "Most people scratch the surface and leave thousands of points unclaimed. "
        "Here's how to use it properly."
    ),
    "money/residence-tax-japan-foreigners.md": (
        "Residence tax in Japan arrives as a surprise for most foreigners in their second year — it's a substantial bill that many people aren't financially prepared for. "
        "Understanding how it works before it arrives makes it much easier to manage. "
        "Here's what residence tax is and how to plan for it."
    ),
    "money/saving-money-in-japan-tips.md": (
        "Japan can be extremely affordable if you live like a resident rather than a tourist. "
        "The gap between how much foreigners spend and how much they could spend is often enormous. "
        "Here are the practical habits that actually make a difference to your monthly budget."
    ),
    "money/side-income-japan-foreigner.md": (
        "Earning side income in Japan as a foreigner is possible — but your visa type determines what's allowed, and going outside those limits has serious consequences. "
        "Know the rules before you start. "
        "Here's a practical guide to legal side income for foreigners in Japan."
    ),
    "money/tax-treaty-japan-foreigner.md": (
        "Japan has tax treaties with dozens of countries that can dramatically reduce what you owe — or prevent you from being taxed twice on the same income. "
        "Most foreigners don't know whether their country has a treaty with Japan or how to use it. "
        "Here's how to find out and what to do."
    ),
    "money/wise-japan-guide.md": (
        "Wise is one of the best tools available for foreigners managing money in Japan — low fees, real exchange rates, and multi-currency accounts that work across borders. "
        "But it has specific limitations in the Japanese market that are worth knowing before you rely on it. "
        "Here's the full picture."
    ),

    # ===== VISA =====
    "visa/business-manager-visa-japan.md": (
        "Japan's Business Manager visa allows foreigners to start or manage a business here — but the requirements are specific and the threshold is higher than most people expect. "
        "Getting the application wrong delays everything by months. "
        "Here's a complete guide to the Business Manager visa."
    ),
    "visa/dependent-visa-japan-guide.md": (
        "Bringing your family to Japan requires a dependent visa — and the process is more involved than most people anticipate when they start planning. "
        "Understanding the requirements early prevents delays that can keep families separated for months. "
        "Here's how the dependent visa process works."
    ),
    "visa/getting-married-japan-foreigner.md": (
        "Getting married in Japan as a foreigner involves two separate processes — a Japanese legal registration and the documentation from your home country — and missing either creates problems. "
        "The process is manageable when you know what's required. "
        "Here's a step-by-step guide to getting married in Japan."
    ),
    "visa/highly-skilled-professional-visa-japan.md": (
        "Japan's Highly Skilled Professional visa offers some of the best benefits in the Japanese immigration system — faster permanent residency, more flexibility, and no job-category restrictions. "
        "Most qualified applicants don't know they're eligible. "
        "Here's how the points system works and how to apply."
    ),
    "visa/how-to-change-visa-status-japan.md": (
        "Changing your visa status from within Japan is possible — but the requirements differ significantly depending on which visa you're switching from and to. "
        "An error in the application can result in weeks of delay or rejection. "
        "Here's how the process works."
    ),
    "visa/how-to-get-permanent-residency-japan.md": (
        "Permanent residency in Japan is a genuine milestone — it removes most of the restrictions that come with a work visa and dramatically simplifies your life here. "
        "But the path is long and the application is detail-heavy. "
        "Here's exactly how to qualify and what the process involves."
    ),
    "visa/how-to-get-work-visa-japan.md": (
        "Getting a work visa for Japan is structured and transparent — if you have the right employer and the right background, the path is clear. "
        "Most people who struggle do so because they misunderstand one specific part of the process. "
        "Here's a step-by-step guide that covers the whole thing."
    ),
    "visa/how-to-renew-work-visa-japan.md": (
        "Work visa renewal in Japan is a process most people handle correctly — but the small mistakes that trip people up can result in a gap in legal status that creates real problems. "
        "Start the process earlier than you think you need to. "
        "Here's exactly how renewal works."
    ),
    "visa/japanese-citizenship-naturalization.md": (
        "Naturalization in Japan is possible for long-term residents — but the requirements are demanding, the timeline is long, and the decision to pursue it is significant. "
        "Japan does not recognize dual citizenship, which changes the calculation for most people. "
        "Here's an honest guide to what naturalization involves."
    ),
    "visa/japanese-residence-card-guide.md": (
        "Your residence card is the most important document you carry in Japan — more than your passport for daily purposes. "
        "Understanding what it contains, when to update it, and the consequences of letting it expire protects your legal status here. "
        "Here's everything you need to know."
    ),
    "visa/permanent-residency-japan-guide.md": (
        "Permanent residency in Japan changes everything — no job-category restrictions, no employer dependency, no renewal anxiety. "
        "It's the most significant upgrade available in the Japanese immigration system. "
        "Here's a complete guide to qualifying and applying."
    ),
    "visa/spouse-dependent-visa-japan.md": (
        "The spouse/dependent visa is one of the most flexible in Japan's immigration system — it allows work without employer sponsorship and is renewable as long as the sponsoring resident maintains their status. "
        "Getting the application right the first time matters. "
        "Here's how it works."
    ),
    "visa/spouse-visa-japan-guide.md": (
        "A spouse visa in Japan grants significant flexibility — the right to live and work without a separate work visa. "
        "But the application requires solid documentation of your relationship, and immigration officers look carefully at the details. "
        "Here's a complete guide to the spouse visa application."
    ),
    "visa/student-visa-japan-guide.md": (
        "Japan's student visa is the starting point for thousands of foreigners who want to study the language, attend university, or explore Japan before making a longer commitment. "
        "The rules on working part-time, changing status, and extending your stay are specific and important. "
        "Here's everything you need to know."
    ),
    "visa/tourist-visa-visa-free-japan.md": (
        "Japan allows visa-free entry for citizens of over 60 countries — which means most visitors arrive without knowing the rules on length of stay, extension, or what activities are prohibited. "
        "Here's what you're actually allowed to do on a tourist entry to Japan."
    ),
    "visa/types-of-work-visa-japan-explained.md": (
        "Japan has more work visa categories than most countries, and choosing the wrong one — or misunderstanding which one applies to your situation — is a common and costly mistake. "
        "Here's a plain-English breakdown of every major work visa type in Japan."
    ),
    "visa/visa-renewal-mistakes-japan.md": (
        "Visa renewal mistakes in Japan range from minor to disqualifying — and most of them are entirely avoidable. "
        "A rejected renewal or a lapse in status creates problems that take months to resolve. "
        "Here are the mistakes people make most often and how to avoid them."
    ),
    "visa/working-holiday-visa-japan.md": (
        "Japan's working holiday visa is one of the best deals in Japanese immigration — legal work permission, flexible movement, and up to a year in the country. "
        "The catch is that it's only available to citizens of specific countries, and the slots fill quickly. "
        "Here's everything you need to know to apply."
    ),
}


def rewrite_intro(filepath, new_intro):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Extract frontmatter
    fm_match = re.match(r'^(---.*?---\s*)', content, re.DOTALL)
    if not fm_match:
        print(f"  SKIP (no frontmatter): {filepath}")
        return False

    fm = fm_match.group(1)
    rest = content[len(fm):]

    # Split into intro and body (## onwards)
    parts = re.split(r'(?=^##\s)', rest, maxsplit=1, flags=re.MULTILINE)
    old_intro = parts[0]
    body = parts[1] if len(parts) > 1 else ''

    # Determine separator based on original intro
    if re.search(r'\n---\n', old_intro):
        separator = '\n\n---\n\n'
    else:
        separator = '\n\n'

    if body:
        new_content = fm + new_intro + separator + body
    else:
        new_content = fm + new_intro + '\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True


def main():
    content_dir = r"C:\Users\mohho\OneDrive\デスクトップ\expatjapan\content"
    success = 0
    skipped = 0
    errors = []

    for rel_path, new_intro in INTROS.items():
        filepath = os.path.join(content_dir, rel_path)
        if not os.path.exists(filepath):
            print(f"  NOT FOUND: {rel_path}")
            skipped += 1
            continue
        try:
            ok = rewrite_intro(filepath, new_intro)
            if ok:
                print(f"  OK: {rel_path}")
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {rel_path} — {e}")
            errors.append((rel_path, str(e)))

    print(f"\n=== Done: {success} rewritten, {skipped} skipped, {len(errors)} errors ===")
    if errors:
        for p, e in errors:
            print(f"  ERROR: {p}: {e}")


if __name__ == '__main__':
    main()
