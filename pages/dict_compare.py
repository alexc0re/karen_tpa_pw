import random
import re
from typing import Dict, List, Any, Optional, Union

PriceDict = Dict[str, Dict[str, List[str]]]


def gachi():
    gachi_videos = ['https://www.youtube.com/watch?v=AIQZ_3xWosc', 'https://www.youtube.com/watch?v=johcE5s525M',
                    'https://www.youtube.com/watch?v=XWDdMVlhpwM&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'https://www.youtube.com/watch?v=frfZyKIHPuQ&t=40s&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'www.youtube.com/watch?v=fUdsmUbs3s0']
    return random.choice(gachi_videos)


def parse_price(value: str):
    # """Перетворює '\$1,056.00' або '\$904.0‘' у float 1056.0, 904.0 (або None, якщо не парситься)."""
    if value is None:
        return None
    s = str(value).strip()
    # виправляємо «криві» лапки
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # лишаємо цифри, кому, крапку, мінус
    s = re.sub(r"[^0-9,.\-]", "", s)
    # прибираємо коми тисяч
    s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def normalize_prices(lst: List[str]) -> List[float]:
    return [p for p in (parse_price(x) for x in (lst or [])) if p is not None]


def compare_and_format(old: PriceDict, new: PriceDict) -> str:
    old_products = set(old.keys())
    new_products = set(new.keys())

    added_products = sorted(new_products - old_products)
    removed_products = sorted(old_products - new_products)
    common_products = sorted(old_products & new_products)

    lines: List[str] = []

    # Додані товари (з усіма позиціями і цінами як у new)
    for product in added_products:
        lines.append(f"\n*Added product:* {product}")
        variants = new.get(product, {})
        for variant, prices in variants.items():
            nums = normalize_prices(prices)
            # якщо кілька цін — виведемо всі
            if len(nums) == 1:
                lines.append(f"  - {variant}: {nums[0]}")
            else:
                lines.append(f"  - {variant}: {', '.join(str(x) for x in nums)}")

    # Видалені товари (з усіма позиціями і цінами як у old)
    for product in removed_products:
        lines.append(f"\n*Deleted product:* {product}")
        variants = old.get(product, {})
        for variant, prices in variants.items():
            nums = normalize_prices(prices)
            if len(nums) == 1:
                lines.append(f"  - {variant}: {nums[0]}")
            else:
                lines.append(f"  - {variant}: {', '.join(str(x) for x in nums)}")

    # Зміни цін по спільних товарах
    for product in common_products:
        old_variants = old.get(product, {}) or {}
        new_variants = new.get(product, {}) or {}

        shared_variants = set(old_variants.keys()) & set(new_variants.keys())

        for variant in sorted(shared_variants):
            old_nums = normalize_prices(old_variants.get(variant))
            new_nums = normalize_prices(new_variants.get(variant))

            # Порівнюємо як списки. Якщо довжина 1, виводимо у вашому форматі "зі X на Y"
            if len(old_nums) == 1 and len(new_nums) == 1:
                if old_nums[0] != new_nums[0]:
                    lines.append(f"\n*Price change*  {product} {variant} *from* {old_nums[0]}$  to ->  {new_nums[0]}$")
            else:
                # Якщо вказано кілька значень — порівняємо списки повністю
                if len(old_nums) != len(new_nums) or any(a != b for a, b in zip(old_nums, new_nums)):
                    lines.append(
                        f"\n*Price change* {product}$ -> {variant}$ "
                        f"*from* [{', '.join(map(str, old_nums))}]$ -> [{', '.join(map(str, new_nums))}]$"
                    )

        # Також можна опціонально виводити додані/видалені варіанти у спільних товарах:
        # added_vars = sorted(set(new_variants) - set(old_variants))
        # removed_vars = sorted(set(old_variants) - set(new_variants))
        # for v in added_vars:
        #     nums = normalize_prices(new_variants[v])
        #     lines.append(f"додана позиція у {product}: {v} = {', '.join(map(str, nums))}")
        # for v in removed_vars:
        #     nums = normalize_prices(old_variants[v])
        #     lines.append(f"видалена позиція у {product}: {v} = {', '.join(map(str, nums))}")

    return lines
