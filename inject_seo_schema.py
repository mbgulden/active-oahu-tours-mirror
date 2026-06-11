#!/usr/bin/env python3
"""
GRO-1208: Inject HowTo schema, FAQPage schema, and AEO Quick Answer blocks
into Active Oahu Tours mirror site pages for Google AI Overviews visibility.

Three phases:
  1. HowTo schema for instruction/guide pages
  2. FAQPage schema where FAQ sections exist
  3. AEO Quick Answer blocks on top-20 pages (visible HTML + FAQPage schema)
"""

import os
import re
import json

SITE_ROOT = "/home/ubuntu/work/active-oahu-tours-mirror/site"

# ── Phase 1: HowTo Schema ───────────────────────────────────────────────────

HOWTO_PAGES = [
    {
        "path": "guides/ocean-kayaking-beginners-oahu/index.html",
        "name": "How to Go Ocean Kayaking on Oahu (Beginner's Guide)",
        "description": "Everything first-time kayakers need to know: best beginner spots, gear checklist, safety tips, and how to book your first ocean kayak trip on Oahu.",
        "steps": [
            {"name": "Choose Your Kayaking Spot", "text": "Pick from Oahu's best beginner-friendly spots: Kailua Bay for calm protected waters, Chinaman's Hat for iconic island views, or Kahana River for rainforest scenery."},
            {"name": "Check Weather and Tide Conditions", "text": "Monitor wind speeds (stay below 15 mph for beginners), check tide charts for your chosen location, and confirm no storm warnings are active."},
            {"name": "Gather Essential Gear", "text": "You'll need a tandem or single kayak, life jacket (PFD), paddle, dry bag for valuables, sunscreen, water, hat, and water shoes or sandals with straps."},
            {"name": "Get On-Site Instruction", "text": "Active Oahu provides private instruction before you launch: paddling technique, safety protocols, how to re-enter your kayak from the water, and local navigation tips."},
            {"name": "Launch and Paddle", "text": "Launch from the beach into calm water. Paddle at a relaxed pace — most routes take 20-40 minutes each way. Stay within sight of shore and follow your planned route."},
            {"name": "Explore and Return Safely", "text": "Enjoy your destination — hike, snorkel, or relax. Allow equal time for return. Paddle back, beach your kayak, and return gear to the pickup point."},
        ],
        "totalTime": "PT4H",
        "url": "https://activeoahutours.com/guides/ocean-kayaking-beginners-oahu/",
    },
    {
        "path": "kayak-safety-guide/index.html",
        "name": "Oahu Kayak Safety Guide",
        "description": "Essential safety information for kayaking on Oahu: wind conditions, tide charts, capsize recovery, emergency contacts, and when NOT to go out.",
        "steps": [
            {"name": "Check Wind Conditions", "text": "Oahu's trade winds typically blow 10-25 mph. Winds above 20 mph create dangerous chop. Check NOAA marine forecast before heading out. Morning paddles (before 11am) are usually calmer."},
            {"name": "Review Tide Charts", "text": "Low tide can expose reefs and make launching difficult. High tide provides easier access but stronger currents. Check local tide charts for your launch location and plan accordingly."},
            {"name": "Wear Your Life Jacket", "text": "Always wear a properly fitted USCG-approved life jacket (PFD) while kayaking. Hawaii law requires a PFD for each person on board."},
            {"name": "Know Capsize Recovery", "text": "If you capsize: stay with your kayak, keep your PFD on, signal for help if needed. Practice the 'T-rescue' technique with a partner: one kayak stabilizes while the other re-enters."},
            {"name": "Carry Emergency Gear", "text": "Bring a whistle, waterproof phone case, and know emergency numbers: Coast Guard VHF Channel 16, Honolulu Fire Department Ocean Safety (808-723-7114), and 911."},
        ],
        "totalTime": "PT15M",
        "url": "https://activeoahutours.com/kayak-safety-guide/",
    },
    {
        "path": "sharks-cove-snorkeling-guide/index.html",
        "name": "How to Snorkel at Sharks Cove on Oahu's North Shore",
        "description": "Complete guide to snorkeling Sharks Cove: best conditions, marine life to see, essential gear, and safety tips for this world-class snorkel spot.",
        "steps": [
            {"name": "Choose the Right Season and Time", "text": "Sharks Cove is best May through September when North Shore surf is calm. Arrive before 9am for best visibility and parking. Avoid winter months when surf exceeds 4 feet."},
            {"name": "Gather Snorkel Gear", "text": "You'll need a mask, snorkel, fins, and reef-safe sunscreen. A rash guard provides sun protection and warmth. Active Oahu rents complete snorkel sets including prescription masks."},
            {"name": "Enter the Water Safely", "text": "Enter from the sandy entry on the right side of the cove. Watch your step on volcanic rock — water shoes help. Wade in slowly and check for sea urchins in crevices."},
            {"name": "Explore the Marine Life", "text": "Look for Hawaiian green sea turtles, parrotfish, butterflyfish, triggerfish, moray eels, and octopus. Stay at least 10 feet from turtles. The left side has deeper water and larger fish."},
            {"name": "Practice Reef-Safe Snorkeling", "text": "Don't touch or stand on coral. Don't feed fish. Use reef-safe sunscreen. Keep fins up when swimming over shallow reef. Stay within the protected cove boundaries."},
        ],
        "totalTime": "PT3H",
        "url": "https://activeoahutours.com/sharks-cove-snorkeling-guide/",
    },
    {
        "path": "oahu-launch-guide/index.html",
        "name": "Oahu Kayak Launch Guide — Best Launch Spots & Conditions",
        "description": "Where to launch your kayak on Oahu: best beach launches, parking, amenities, and what to expect at each location.",
        "steps": [
            {"name": "Choose Your Launch Location", "text": "Select from Kailua Beach Park (calm, lifeguards, restrooms), Kualoa Regional Park (Chinaman's Hat access), Kahana Bay (river launch), or Haleiwa Beach Park (North Shore)."},
            {"name": "Check Launch Conditions", "text": "Review wind direction, swell height, and tide level for your chosen launch. Offshore winds can make return difficult. Check the surf report before heading out."},
            {"name": "Prepare Your Kayak and Gear", "text": "Load kayak onto vehicle with proper pads and straps. Pack all gear in dry bags. Arrive early — popular launches fill up by 9am on weekends."},
            {"name": "Launch and Beach Protocol", "text": "Launch from designated areas only. Give swimmers and surfers plenty of space. When beaching, pull kayak fully above the high-tide line. Respect private property boundaries."},
        ],
        "totalTime": "PT10M",
        "url": "https://activeoahutours.com/oahu-launch-guide/",
    },
    {
        "path": "what-to-bring/index.html",
        "name": "What to Bring on Your Oahu Kayak Adventure — Packing Checklist",
        "description": "Complete packing list for Oahu kayaking: essential gear, sun protection, food and water, and what NOT to bring.",
        "steps": [
            {"name": "Pack Sun Protection", "text": "Reef-safe sunscreen (SPF 30+), polarized sunglasses with strap, wide-brim hat or cap with clip, and UV-protective rash guard or long-sleeve shirt."},
            {"name": "Bring Hydration and Snacks", "text": "At least 1 liter of water per person for a half-day trip. Bring more for full-day adventures. Pack high-energy snacks: granola bars, fruit, nuts, or sandwiches in a waterproof container."},
            {"name": "Protect Your Valuables", "text": "Use a dry bag for phone, keys, wallet, and camera. Bring a waterproof phone case with lanyard. Leave jewelry and watches at home — the ocean claims them."},
            {"name": "Wear the Right Clothing", "text": "Quick-dry shorts or swimsuit, water shoes or sandals with heel straps, and a light windbreaker if paddling in winter (Nov-Mar). Avoid cotton — it stays wet and cold."},
            {"name": "Don't Forget Safety Gear", "text": "Life jacket (provided by Active Oahu), whistle, waterproof flashlight if near dusk, and a small first-aid kit with bandages and antiseptic wipes."},
        ],
        "totalTime": "PT10M",
        "url": "https://activeoahutours.com/what-to-bring/",
    },
]

# ── Phase 2: FAQPage Schema ─────────────────────────────────────────────────

FAQ_PAGES = [
    {
        "path": "faq-oahu-beach-gear-rentals/index.html",
        "url": "https://activeoahutours.com/faq-oahu-beach-gear-rentals/",
        "questions": [
            {"q": "Can you accommodate large groups or events?", "a": "Yes. Active Oahu has successfully worked with multiple large groups and corporate events and can help organize and facilitate activities. Contact us at info@activeoahutours.com."},
            {"q": "Can we rent gear for just a couple of hours for less than the 4-hour or daily rate?", "a": "No, we charge for 4 hours minimum, but you can end your daily or 4-hour rental early with no problem as long as you notify us either when you pick up the equipment or when you make the booking."},
            {"q": "How long is the Full Day rental?", "a": "From 8 am to 4:30 pm. Make sure you are back at our shop before 5 pm. If you want your beach gear rentals for longer than daytime hours, get a 2-day rental."},
            {"q": "Where can you deliver?", "a": "We deliver to private addresses around Kailua and up to Sunset Beach on the North Shore. We also deliver out to Haleiwa for larger orders. We are based out of Kailua, so the majority of our delivery locations are less than 30 minutes away."},
            {"q": "Where should we meet you?", "a": "Meet at our storefront in Kailua (134B Hamakua Drive, Kailua, HI 96734) or specify the private address or vacation rental where we will deliver. If we need clarification after you book, we will email, call or text you."},
        ],
    },
    {
        "path": "faq/faq-chinamans-hat-kayak-hike/index.html",
        "url": "https://activeoahutours.com/faq/faq-chinamans-hat-kayak-hike/",
        "questions": [
            {"q": "How long is the paddle to Chinaman's Hat?", "a": "The paddle from Kualoa Regional Park to Mokolii (Chinaman's Hat) takes approximately 20-30 minutes each way at a relaxed pace, depending on wind and current conditions."},
            {"q": "Can I hike to the top of Chinaman's Hat?", "a": "Yes, there is a trail to the summit. The hike is steep and rocky — wear sturdy shoes. The trail takes about 20-30 minutes to climb and offers panoramic views of Kaneohe Bay and the Ko'olau Mountains."},
            {"q": "Do I need a permit to kayak to Chinaman's Hat?", "a": "No permit is required to kayak to Mokolii or hike the island. However, respect the area as a culturally significant site and don't remove anything from the island."},
            {"q": "What's the best time to kayak to Chinaman's Hat?", "a": "Morning (before 11am) offers the calmest water and best conditions. Check the tide chart — low tide can make the beach landing tricky. Weekdays are less crowded than weekends."},
        ],
    },
    {
        "path": "faq/index.html",
        "url": "https://activeoahutours.com/faq/",
        "questions": [
            {"q": "What types of tours and rentals does Active Oahu offer?", "a": "We offer self-guided kayak tours, guided kayak and e-bike adventures, stand-up paddleboard tours, snorkel excursions, and beach gear rentals including kayaks, SUPs, snorkel sets, beach chairs, umbrellas, and coolers."},
            {"q": "Where is Active Oahu located?", "a": "Our storefront is at 134B Hamakua Drive in Kailua, Oahu. We deliver kayaks and beach gear to locations across Windward Oahu, from Kailua to the North Shore."},
            {"q": "Do I need kayaking experience?", "a": "No experience is necessary for most of our tours. We provide on-site instruction before you launch, and our routes are chosen for beginner-friendly conditions. You should be comfortable in water and able to swim."},
            {"q": "How do I book a tour or rental?", "a": "Book online at activeoahutours.com, call us at (808) 498-1894, or visit our Kailua storefront. We recommend booking at least 24 hours in advance, especially during peak seasons."},
        ],
    },
    {
        "path": "paa-answers/index.html",
        "url": "https://activeoahutours.com/paa-answers/",
        "questions": [
            {"q": "What is the best kayaking spot on Oahu for beginners?", "a": "Kailua Bay is the best spot for beginners — it offers protected calm waters, easy beach launches, lifeguards, and beautiful views of the Mokulua Islands. The paddle to Flat Island (Popoia) takes about 20 minutes."},
            {"q": "When is the best time of year to kayak on Oahu?", "a": "Summer months (May-September) offer the calmest ocean conditions, especially on the North and Windward shores. Winter brings larger north swells but the windward side often remains paddleable in the mornings."},
            {"q": "Do I need to book in advance?", "a": "Yes, we strongly recommend booking at least 24 hours in advance. During peak seasons (summer, holidays), popular tours and rentals can book out 3-5 days ahead. Walk-ins are welcome but availability is not guaranteed."},
        ],
    },
    {
        "path": "guides/ocean-kayaking-beginners-oahu/index.html",
        "url": "https://activeoahutours.com/guides/ocean-kayaking-beginners-oahu/",
        "questions": [
            {"q": "How physically fit do I need to be for ocean kayaking?", "a": "Ocean kayaking is a moderate activity. Paddling to Flat Island takes about 20 minutes at a relaxed pace — most people find it easier than expected. You should be comfortable in water and able to climb back onto a kayak. If you can walk for an hour, you can kayak for an hour."},
            {"q": "What happens if the weather turns bad?", "a": "Active Oahu monitors conditions closely and will cancel or reschedule if conditions are unsafe. Wind speeds above 20 mph or lightning in the area will cancel trips. You will receive a full refund or free reschedule."},
            {"q": "Do I need to know how to swim?", "a": "You should be comfortable in the water, but you don't need to be a strong swimmer. You will be wearing a life jacket the entire time, and most routes stay in water shallow enough to stand."},
            {"q": "Can I bring my phone or camera?", "a": "Yes — but put it in a waterproof case or dry bag. Kayaks are stable, but splashing is common. A floating wrist strap adds extra security."},
        ],
    },
    {
        "path": "beach-gear-rentals/index.html",
        "url": "https://activeoahutours.com/beach-gear-rentals/",
        "questions": [
            {"q": "What beach gear can I rent from Active Oahu?", "a": "We rent tandem kayaks, stand-up paddleboards (SUPs), snorkel sets (mask, fins, snorkel), beach chairs, umbrellas, coolers, dry bags, life vests, kayak anchors, surfboards, boogie boards, and kayak transport trolleys."},
            {"q": "Do you deliver beach gear to my location?", "a": "Yes, we deliver to private addresses, vacation rentals, and hotels in Kailua and up to Sunset Beach on the North Shore. Delivery is included in rental rates for most locations."},
        ],
    },
    {
        "path": "kayak-rentals/index.html",
        "url": "https://activeoahutours.com/kayak-rentals/",
        "questions": [
            {"q": "What types of kayaks do you rent?", "a": "We rent tandem (2-person) sit-on-top ocean kayaks — the most stable and beginner-friendly type for Hawaii's waters. They're easy to board from the water and virtually unsinkable."},
            {"q": "What's included with a kayak rental?", "a": "Every kayak rental includes the kayak, two paddles, two USCG-approved life jackets, padded seat backs, a dry bag, and on-site instruction. Foam pads and straps for vehicle transport are also provided."},
        ],
    },
    {
        "path": "electric-bike-rentals/index.html",
        "url": "https://activeoahutours.com/electric-bike-rentals/",
        "questions": [
            {"q": "What e-bikes do you rent?", "a": "We rent pedal-assist electric bikes perfect for exploring Kailua, Lanikai, and the Windward coast. They have a range of 30-50 miles on a charge and come with helmets and locks."},
            {"q": "Can I tow a kayak with an e-bike?", "a": "Yes! Active Oahu provides e-bike kayak trailers that let you tow kayaks from our Kailua storefront to Kailua Beach (about 1 mile away). It's a popular add-on for self-guided kayak tours."},
        ],
    },
    {
        "path": "multi-day-rentals/index.html",
        "url": "https://activeoahutours.com/multi-day-rentals/",
        "questions": [
            {"q": "Do you offer multi-day rental discounts?", "a": "Yes, multi-day rentals get discounted daily rates. The longer you rent, the lower the per-day cost. Multi-day rentals are perfect for exploring different Oahu locations throughout your trip."},
            {"q": "How does multi-day rental pickup and return work?", "a": "We deliver on your first day and pick up on your last day at the scheduled times. You keep the equipment for the full rental period. Early morning pickup before flights is available with advance notice."},
        ],
    },
]

# ── Phase 3: AEO Quick Answer Blocks ────────────────────────────────────────

# Top-20 pages by traffic/revenue potential, each with a concise 50-75 word answer
AEO_PAGES = [
    {
        "path": "activities/chinamans-hat-self-guided-oahu-kayak-tour/index.html",
        "question": "What is the Chinaman's Hat kayak tour on Oahu?",
        "answer": "Active Oahu's Chinaman's Hat Self-Guided Kayak Tour lets you paddle across Kaneohe Bay to Mokolii Island (Chinaman's Hat). You'll get a tandem kayak, safety gear, dry bag, and private instruction before launching. Once there, hike to the summit for panoramic views of the Ko'olau Mountains and Kaneohe Bay. Book at activeoahutours.com or call (808) 498-1894.",
    },
    {
        "path": "activities/kailua-bay-mokulua-island-self-guided-kayak-tour/index.html",
        "question": "How do I kayak to the Mokulua Islands from Kailua?",
        "answer": "Active Oahu provides a self-guided kayak tour to the Mokulua Islands from Kailua Beach. We supply kayaks, life vests, dry bags, permits for Moku Nui bird sanctuary, and on-site instruction. The paddle takes 30-45 minutes each way. Explore tide pools, spot sea turtles, and enjoy one of Oahu's most iconic adventures. Call (808) 498-1894 to book.",
    },
    {
        "path": "index.html",
        "question": "What does Active Oahu Tours offer for kayaking and beach rentals?",
        "answer": "Active Oahu provides self-guided kayak tours, guided adventures, e-bike rentals, and beach gear delivery on Oahu's Windward side. We offer kayak rentals, snorkel gear, SUPs, beach chairs, umbrellas, and more — delivered to your door or picked up at our Kailua storefront at 134B Hamakua Drive. Book online or call (808) 498-1894.",
    },
    {
        "path": "activities/kaneohe-sandbar-kayak-ultimate-guide/index.html",
        "question": "What is the best way to kayak to Kaneohe Sandbar?",
        "answer": "Active Oahu offers kayak rentals and delivery for Kaneohe Sandbar adventures. Launch from He'eia Kea Boat Harbor or Kualoa Park, paddle 30-45 minutes to the sandbar, and enjoy this unique floating oasis in Kaneohe Bay. Go at mid-to-low tide for the best sandbar exposure. We provide kayaks, safety gear, and local tips. Book at (808) 498-1894.",
    },
    {
        "path": "activities/rainforest-oahu-kayak-tour.html",
        "question": "What is the Kahana rainforest river kayak tour on Oahu?",
        "answer": "Active Oahu's Kahana Rainforest River Kayak Tour takes you up a calm mountain stream through Kahana Valley, then out into Kahana Bay. This self-guided adventure offers lush jungle scenery, turquoise water, and mountain views with an Amazonian feel. We provide kayaks, paddles, life vests, dry bags, and transport gear. A 40-minute drive from Kailua. Book at activeoahutours.com.",
    },
    {
        "path": "activities/haleiwa-paddleboarding/index.html",
        "question": "Where can I go stand-up paddleboarding on Oahu's North Shore?",
        "answer": "Active Oahu offers SUP rentals and delivery to Haleiwa and the North Shore. Paddle the calm waters of Haleiwa Bay or the Anahulu River where you can spot sea turtles. Summer months (May-September) offer the best conditions for North Shore paddleboarding. We provide boards, paddles, leashes, and life vests. Book online or call (808) 498-1894.",
    },
    {
        "path": "activities/oahu-snorkel-tour/index.html",
        "question": "What are the best snorkeling tours on Oahu?",
        "answer": "Active Oahu offers self-guided snorkel excursions to Oahu's top spots: Sharks Cove on the North Shore (summer only), Lanikai Beach for calm reef snorkeling, and Electric Beach on the West side for advanced snorkelers. We provide complete snorkel sets — masks, fins, snorkels — plus local tips on conditions and marine life. Rental sets include prescription mask options. Book at (808) 498-1894.",
    },
    {
        "path": "activities/aloha-aina-e-bike-adventure/index.html",
        "question": "What is an Oahu e-bike adventure tour?",
        "answer": "Active Oahu's Aloha 'Aina E-Bike Adventure is a self-guided tour exploring Kailua and Lanikai by pedal-assist electric bike. Ride along coastal roads, visit secret beaches, stop at local food spots, and take in views of the Mokulua Islands. Includes e-bike, helmet, lock, route map, and local recommendations. Add a kayak trailer for a combined e-bike + kayak experience. Book at activeoahutours.com.",
    },
    {
        "path": "activities/lanikai-beach-self-guided-snorkel/index.html",
        "question": "How do I snorkel at Lanikai Beach on Oahu?",
        "answer": "Active Oahu rents snorkel sets for Lanikai Beach, one of Oahu's best calm-water snorkeling spots. Enter from the sandy beach and snorkel around the nearshore reef patches. You'll see butterflyfish, parrotfish, tangs, and occasionally sea turtles. Morning offers the clearest visibility. We provide masks, fins, snorkels, and tips on the best entry points. Rent online or at our Kailua storefront.",
    },
    {
        "path": "kayak-rentals/index.html",
        "question": "How much does it cost to rent a kayak on Oahu?",
        "answer": "Active Oahu rents tandem kayaks starting at $69 for 4 hours, with full-day (8am-4:30pm) and multi-day options at discounted rates. All rentals include paddles, life vests, seat backs, dry bag, on-site instruction, and foam pads with straps for vehicle transport. Delivery available to Kailua and North Shore locations. Multi-day rentals offer the best value. Book at activeoahutours.com.",
    },
    {
        "path": "activities/chinamans-hat-kayak-rentals/index.html",
        "question": "Where can I rent a kayak near Chinaman's Hat?",
        "answer": "Active Oahu rents kayaks for Chinaman's Hat (Mokolii) adventures. Pick up at our Kailua storefront at 134B Hamakua Drive, then drive 25 minutes to Kualoa Regional Park to launch. We provide tandem kayaks, paddles, life vests, dry bags, foam pads with straps for your vehicle, and on-site instruction before you go. Book online or call (808) 498-1894.",
    },
    {
        "path": "sharks-cove-snorkeling-guide/index.html",
        "question": "What should I know before snorkeling at Sharks Cove on Oahu?",
        "answer": "Sharks Cove on Oahu's North Shore is a world-class snorkeling spot best visited May-September when the surf is calm. Arrive before 9am for parking and best visibility. You'll see sea turtles, parrotfish, butterflyfish, eels, and octopus. Wear reef-safe sunscreen, water shoes for the rocky entry, and never touch the coral. Active Oahu rents complete snorkel sets. The cove is protected — stay within its boundaries.",
    },
    {
        "path": "guides/sea-turtles-oahu/index.html",
        "question": "Where can I see sea turtles on Oahu?",
        "answer": "You can see Hawaiian green sea turtles (honu) at Laniakea Beach on the North Shore, Kailua Beach Park, Lanikai Beach, and while kayaking to the Mokulua Islands or Chinaman's Hat. Summer offers the calmest water for turtle viewing. Stay at least 10 feet away — it's Hawaii state law. Never touch, chase, or feed turtles. Active Oahu's kayak and snorkel tours frequently encounter turtles. Call (808) 498-1894.",
    },
    {
        "path": "guides/kailua-beach-park/index.html",
        "question": "What makes Kailua Beach Park the best beach on Oahu?",
        "answer": "Kailua Beach Park offers 2.5 miles of powdery white sand, calm turquoise water protected by an offshore reef, lifeguards, restrooms, showers, and picnic areas. It's ideal for swimming, kayaking to the Mokulua Islands, paddleboarding, and beginner-friendly ocean activities. Parking is free but fills early on weekends. Active Oahu's storefront is one mile away at 134B Hamakua Drive.",
    },
    {
        "path": "guides/lanikai-beach/index.html",
        "question": "Why is Lanikai Beach considered one of Oahu's best beaches?",
        "answer": "Lanikai Beach features powdery white sand and postcard-perfect views of the Mokulua Islands. Its calm, clear water makes it ideal for swimming, snorkeling, and kayaking. The protected offshore reef creates a natural lagoon effect. There are no public restrooms or lifeguards, so come prepared. Access through neighborhood paths — parking is limited. Morning offers the calmest conditions. Active Oahu delivers kayaks and gear nearby.",
    },
    {
        "path": "tours/index.html",
        "question": "What types of tours does Active Oahu offer on Oahu?",
        "answer": "Active Oahu offers self-guided kayak tours to Chinaman's Hat and the Mokulua Islands, guided kayak and e-bike combo tours, rainforest river paddling, stand-up paddleboarding, snorkeling excursions, and e-bike adventures. All tours include equipment, instruction, and local knowledge. Self-guided tours give you freedom to explore at your own pace. Guided tours add expert narration and permit handling. Browse tours at activeoahutours.com.",
    },
    {
        "path": "multi-day-kayak-and-beach-gear-rentals/index.html",
        "question": "Can I rent kayaks and beach gear for multiple days on Oahu?",
        "answer": "Yes, Active Oahu offers multi-day kayak and beach gear rentals with discounted rates. Keep your kayak, SUP, snorkel set, beach chairs, and umbrella for your entire trip — we deliver on day one and pick up on your last day. Perfect for exploring different Oahu beaches and kayaking spots throughout your vacation. Multi-day rentals offer the best value. Book at activeoahutours.com or call (808) 498-1894.",
    },
    {
        "path": "activities/guided-mokulua-islands-kayak-tour-and-e-bike-adventure/index.html",
        "question": "What is the Guided Mokulua Islands Kayak and E-Bike Adventure?",
        "answer": "Active Oahu's signature guided tour combines kayaking to the Mokulua Islands with an e-bike adventure. Our expert guide leads you across Kailua Bay to Moku Nui bird sanctuary (permits included), exploring tide pools and spotting sea turtles and monk seals. After 5 hours on the water, you'll tour Kailua by e-bike. Suitable for active kayakers 13+. Book this premium experience at activeoahutours.com.",
    },
    {
        "path": "activities/kaneohe-sandbar-kayak-rentals/index.html",
        "question": "How do I rent a kayak for Kaneohe Sandbar?",
        "answer": "Active Oahu provides kayak rentals with delivery for Kaneohe Sandbar adventures. The sandbar is a unique mid-bay destination in Kaneohe Bay — a stretch of shallow water where you can stand waist-deep surrounded by ocean. Launch from He'eia Kea Boat Harbor or Kualoa Park. Visit at mid-to-low tide for the best sandbar experience. We provide all gear including kayaks, paddles, and life vests. Book at activeoahutours.com.",
    },
    {
        "path": "activities/rainforest-oahu-stand-up-paddle-boarding/index.html",
        "question": "Where can I paddleboard on a river on Oahu?",
        "answer": "Active Oahu's Rainforest Stand Up Paddle Board Self-Guided Tour takes you up the calm Kahana River through a lush rainforest valley. This unique SUP experience offers mountain stream paddling with jungle scenery — no ocean swells, perfect for beginners. We provide paddleboards, paddles, leashes, life vests, and vehicle transport gear. A 40-minute drive from our Kailua storefront. Book online at activeoahutours.com or call (808) 498-1894.",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Schema Builder Functions
# ═══════════════════════════════════════════════════════════════════════════════

def build_howto_schema(page):
    """Build HowTo schema JSON-LD."""
    steps = []
    for i, step in enumerate(page["steps"], 1):
        steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": step["name"],
            "text": step["text"],
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": page["name"],
        "description": page["description"],
        "step": steps,
        "totalTime": page["totalTime"],
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_faq_schema(questions):
    """Build FAQPage schema JSON-LD."""
    main_entities = []
    for qa in questions:
        main_entities.append({
            "@type": "Question",
            "name": qa["q"],
            "acceptedAnswer": {
                "@type": "Answer",
                "text": qa["a"],
            },
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entities,
    }
    return json.dumps(schema, ensure_ascii=False, indent=2)


def build_aeo_block(page):
    """Build AEO Quick Answer HTML block + FAQPage schema with single question."""
    block_html = f"""<!-- AEO Quick Answer Block (GRO-1208) -->
<div class="aeo-quick-answer" style="background:#f0f7fb; border-left:4px solid #006699; padding:16px 20px; margin:20px 0; border-radius:4px;">
  <h2 style="margin:0 0 8px 0; font-size:1.1em; color:#006699;">Quick Answer</h2>
  <p style="margin:0; font-size:0.95em; line-height:1.5;">{page["answer"]}</p>
</div>
<!-- End AEO Quick Answer -->"""

    # Also build FAQPage schema for the single Q&A
    schema = build_faq_schema([
        {"q": page["question"], "a": page["answer"]}
    ])

    schema_block = f'<script type="application/ld+json">\n{schema}\n</script>'
    return block_html, schema_block


def inject_before_head_close(filepath, block):
    """Inject an HTML block just before </head>."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "</head>" not in content:
        return False, "No </head> found"

    new_content = content.replace("</head>", f"{block}\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"Injected {len(block)} chars"


def inject_after_tag(filepath, tag_pattern, block):
    """Inject an HTML block after first occurrence of a tag pattern. Returns (success, message)."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(tag_pattern, content)
    if not match:
        return False, f"Tag pattern not found: {tag_pattern}"

    insert_pos = match.end()
    new_content = content[:insert_pos] + "\n" + block + "\n" + content[insert_pos:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"Injected {len(block)} chars after pattern"


def inject_multiple_blocks(filepath, injections):
    """
    Inject multiple blocks before </head>. injections = list of strings.
    Handles case where some schema may already exist.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "</head>" not in content:
        return False, "No </head> found"

    combined = "\n".join(injections)
    new_content = content.replace("</head>", f"{combined}\n</head>", 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    return True, f"Injected {len(combined)} chars total"


# ═══════════════════════════════════════════════════════════════════════════════
# Main Execution
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    stats = {"howto": 0, "faq": 0, "aeo": 0, "skipped": 0, "failed": 0}

    print("=" * 70)
    print("GRO-1208: SEO Schema Injection — HowTo + FAQPage + AEO Blocks")
    print("=" * 70)

    # ── Phase 1: HowTo Schema ──
    print("\n── Phase 1: HowTo Schema ──")
    for page in HOWTO_PAGES:
        filepath = os.path.join(SITE_ROOT, page["path"])
        if not os.path.isfile(filepath):
            print(f"  ❌ FILE NOT FOUND: {page['path']}")
            stats["failed"] += 1
            continue

        schema_json = build_howto_schema(page)
        schema_block = f'<script type="application/ld+json">\n{schema_json}\n</script>'

        # Check if HowTo schema already exists
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if '"@type":"HowTo"' in content or '"@type": "HowTo"' in content:
            print(f"  ⏭️  SKIP (already has HowTo): {page['path']}")
            stats["skipped"] += 1
            continue

        ok, msg = inject_before_head_close(filepath, schema_block)
        if ok:
            print(f"  ✅ HowTo: {page['path']} ({len(page['steps'])} steps)")
            stats["howto"] += 1
        else:
            print(f"  ❌ FAILED {page['path']}: {msg}")
            stats["failed"] += 1

    # ── Phase 2: FAQPage Schema ──
    print("\n── Phase 2: FAQPage Schema ──")
    for page in FAQ_PAGES:
        filepath = os.path.join(SITE_ROOT, page["path"])
        if not os.path.isfile(filepath):
            print(f"  ❌ FILE NOT FOUND: {page['path']}")
            stats["failed"] += 1
            continue

        schema_json = build_faq_schema(page["questions"])
        schema_block = f'<script type="application/ld+json">\n{schema_json}\n</script>'

        # Check if FAQPage schema already exists
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if '"@type":"FAQPage"' in content or '"@type": "FAQPage"' in content:
            print(f"  ⏭️  SKIP (already has FAQPage): {page['path']}")
            stats["skipped"] += 1
            continue

        ok, msg = inject_before_head_close(filepath, schema_block)
        if ok:
            print(f"  ✅ FAQPage: {page['path']} ({len(page['questions'])} Q&As)")
            stats["faq"] += 1
        else:
            print(f"  ❌ FAILED {page['path']}: {msg}")
            stats["failed"] += 1

    # ── Phase 3: AEO Quick Answer Blocks ──
    print("\n── Phase 3: AEO Quick Answer Blocks ──")
    for page in AEO_PAGES:
        filepath = os.path.join(SITE_ROOT, page["path"])
        if not os.path.isfile(filepath):
            print(f"  ❌ FILE NOT FOUND: {page['path']}")
            stats["failed"] += 1
            continue

        block_html, schema_block = build_aeo_block(page)

        # Check if AEO block already exists
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if "aeo-quick-answer" in content:
            print(f"  ⏭️  SKIP (already has AEO block): {page['path']}")
            stats["skipped"] += 1
            continue

        # Inject FAQPage schema before </head>
        schema_ok, schema_msg = inject_before_head_close(filepath, schema_block)

        # Inject AEO HTML block after <h1>
        h1_pattern = r'<h1[^>]*>.*?</h1>'
        html_ok, html_msg = inject_after_tag(filepath, h1_pattern, block_html)

        # Re-read to verify
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        has_schema = "FAQPage" in content
        has_aeo = "aeo-quick-answer" in content

        if has_schema and has_aeo:
            print(f"  ✅ AEO: {page['path']} (answer: {len(page['answer'])} chars)")
            stats["aeo"] += 1
        else:
            issues = []
            if not has_schema:
                issues.append("schema missing")
            if not has_aeo:
                issues.append("AEO block missing")
            print(f"  ❌ FAILED {page['path']}: {', '.join(issues)}")
            stats["failed"] += 1

    # ── Summary ──
    print(f"\n{'=' * 70}")
    print(f"SUMMARY:")
    print(f"  HowTo schemas added:   {stats['howto']}")
    print(f"  FAQPage schemas added: {stats['faq']}")
    print(f"  AEO blocks added:      {stats['aeo']}")
    print(f"  Skipped (already had): {stats['skipped']}")
    print(f"  Failed:                {stats['failed']}")
    print(f"  TOTAL PAGES TOUCHED:   {stats['howto'] + stats['faq'] + stats['aeo']}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
