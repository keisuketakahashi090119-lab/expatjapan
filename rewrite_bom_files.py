#!/usr/bin/env python3
"""
Rewrite intros for files that have BOM (utf-8-sig encoding).
"""

import re
import os
import sys

INTROS = {
    "culture/japanese-language-school-guide.md": (
        "Choosing the wrong Japanese language school is an expensive mistake that costs you months of progress. "
        "The right school can transform your Japanese — and your life in Japan. "
        "Here's how to evaluate your options and pick the one that actually fits your goals."
    ),
    "daily-life/best-cities-live-japan-foreigners.md": (
        "Choosing the wrong city is a mistake that takes a year to undo. "
        "Japan's major cities are more different from each other than most people expect — in cost, pace, foreigner infrastructure, and job market. "
        "Here's a clear-eyed comparison to help you decide where to actually land."
    ),
    "daily-life/car-insurance-japan-foreigner.md": (
        "Car insurance in Japan is mandatory — and the system works differently than in most countries. "
        "Without the right coverage, a single accident can be financially devastating. "
        "Here's everything you need to know before you get behind the wheel."
    ),
    "daily-life/childcare-nursery-japan-foreigner.md": (
        "Finding nursery care in Japan as a foreigner feels impossible at first — waitlists, paperwork in Japanese, an opaque points system. "
        "But parents who understand how the system works can navigate it far more successfully. "
        "Here's an honest guide to childcare in Japan for foreign families."
    ),
    "daily-life/corporate-housing-shataku-japan.md": (
        "Some Japanese companies offer housing — called shataku — as part of the employment package, and it can save you enormous money. "
        "But the terms vary widely and not everyone knows to ask about it. "
        "Here's what shataku is, who qualifies, and whether it's worth taking."
    ),
    "daily-life/jr-pass-guide-foreigners-japan.md": (
        "The JR Pass costs a significant amount of money. Whether it actually saves you money depends entirely on how you use it. "
        "Many tourists buy it by default and end up overpaying. "
        "Here's the honest math — and when it's actually worth it."
    ),
    "daily-life/living-fukuoka-as-foreigner.md": (
        "Fukuoka keeps appearing on lists of the best cities to live in Asia — and for foreigners, it often outperforms expectations. "
        "Cheap, relaxed, connected to the rest of Japan, and easier to navigate than Tokyo. "
        "Here's an honest look at what life in Fukuoka is actually like."
    ),
    "daily-life/living-osaka-as-foreigner.md": (
        "Osaka has a reputation for being louder, friendlier, and more affordable than Tokyo — and it earns that reputation. "
        "But the reality of living here as a foreigner has its own quirks and challenges. "
        "Here's an honest guide to daily life in Osaka."
    ),
    "jobs/japanese-rirekisho-guide.md": (
        "The rirekisho is Japan's traditional resume format — handwritten, formatted, and unlike anything you've submitted before. "
        "Getting it wrong signals lack of attention to detail before you've even had an interview. "
        "Here's how to complete one properly."
    ),
    "jobs/shukkatsu-guide-japan-foreigner.md": (
        "Shukkatsu — Japan's new graduate job hunting season — operates on a calendar and process that shocks most foreigners encountering it for the first time. "
        "It is highly structured, starts earlier than you'd expect, and has its own rituals and expectations. "
        "Here's how to navigate it as a foreign student or graduate."
    ),
    "jobs/working-japan-without-japanese.md": (
        "Working in Japan without speaking Japanese is possible — but the path is narrower than most people think, and the industries where it works are specific. "
        "Knowing where your skills fit opens real opportunities. "
        "Here's an honest guide to working in Japan without Japanese language ability."
    ),
    "money/atm-guide-foreigners-japan.md": (
        "Japan is still a cash-heavy country, and finding an ATM that actually accepts your foreign card is not as simple as it sounds. "
        "The wrong ATM will decline you at the most inconvenient moment. "
        "Here's exactly which ATMs work for foreigners and how to use them."
    ),
    "money/cost-of-living-japan-2025.md": (
        "Japan's cost of living reputation is outdated. The yen's weakness has made Japan more affordable than most Western countries for many categories of spending — and more expensive in others. "
        "Here's a current, honest breakdown of what life actually costs in Japan in 2025."
    ),
    "money/earthquake-insurance-japan.md": (
        "Standard apartment insurance in Japan does not cover earthquake damage — that requires a separate earthquake insurance policy. "
        "Given Japan's seismic activity, this is not a gap worth leaving open. "
        "Here's how earthquake insurance works and whether you need it."
    ),
    "money/japan-travel-insurance-residents.md": (
        "Japan's national health insurance covers you domestically — but the moment you leave the country, you're uninsured unless you have separate travel coverage. "
        "For residents who travel regularly, the right travel insurance policy matters. "
        "Here's how to choose one."
    ),
    "money/life-insurance-japan-foreigner.md": (
        "Life insurance in Japan is widely available, competitively priced, and accessible to foreign residents — but the range of products is bewildering. "
        "Understanding what you actually need simplifies the decision significantly. "
        "Here's a practical guide to life insurance in Japan for foreigners."
    ),
    "money/pension-lump-sum-refund-japan.md": (
        "When you leave Japan, you may be able to claim a lump-sum refund of the pension contributions you paid — and the window to claim it is short. "
        "Thousands of foreigners leave without claiming money they're entitled to. "
        "Here's how the pension refund works and how to apply."
    ),
    "money/tax-treaty-japan-foreigner.md": (
        "Japan has tax treaties with dozens of countries that can dramatically reduce what you owe — or prevent you from being taxed twice on the same income. "
        "Most foreigners don't know whether their country has a treaty with Japan or how to use it. "
        "Here's how to find out and what to do."
    ),
    "visa/getting-married-japan-foreigner.md": (
        "Getting married in Japan as a foreigner involves two separate processes — a Japanese legal registration and the documentation from your home country — and missing either creates problems. "
        "The process is manageable when you know what's required. "
        "Here's a step-by-step guide to getting married in Japan."
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
}


def rewrite_intro_bom(filepath, new_intro):
    # Read with BOM-aware encoding
    with open(filepath, encoding='utf-8-sig') as f:
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

    # Determine separator
    if re.search(r'\n---\n', old_intro):
        separator = '\n\n---\n\n'
    else:
        separator = '\n\n'

    if body:
        new_content = fm + new_intro + separator + body
    else:
        new_content = fm + new_intro + '\n'

    # Write back WITHOUT BOM, as utf-8
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
            ok = rewrite_intro_bom(filepath, new_intro)
            if ok:
                print(f"  OK: {rel_path}")
                success += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {rel_path} -- {e}")
            errors.append((rel_path, str(e)))

    print(f"\nDone: {success} rewritten, {skipped} skipped, {len(errors)} errors")
    if errors:
        for p, e in errors:
            print(f"  ERROR {p}: {e}")


if __name__ == '__main__':
    main()
