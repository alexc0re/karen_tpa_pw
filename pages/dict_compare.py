import random
from typing import Dict, List, Any, Optional, Union

Number = Union[int, float]


def gachi():
    gachi_videos = ['https://www.youtube.com/watch?v=AIQZ_3xWosc', 'https://www.youtube.com/watch?v=johcE5s525M',
                    'https://www.youtube.com/watch?v=XWDdMVlhpwM&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'https://www.youtube.com/watch?v=frfZyKIHPuQ&t=40s&pp=ygULZ2FjaGkgdmlkZW8%3D',
                    'www.youtube.com/watch?v=fUdsmUbs3s0']
    return random.choice(gachi_videos)


def _parse_price(value: Any) -> Optional[Number]:
    """
    Приймає значення ціни:
      - "$119.0" або "119.0" або 119.0
      - список з одним таким значенням, напр. ["$119.0"]
    Повертає float або None, якщо розпарсити неможливо.
    """
    # Якщо це список типу ["$119.0"], беремо перший елемент
    if isinstance(value, list) and value:
        value = value[0]
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        s = value.strip()
        # прибираємо валютні та зайві символи
        s = s.replace("$", "").replace(",", "").strip()
        try:
            return float(s)
        except ValueError:
            return None
    return None


def _fmt_price(v: Optional[Number]) -> str:
    return "N/A" if v is None else f"${v:,.2f}"


def compare_nested_price_dicts(
        old: Dict[str, Dict[str, List[Any]]],
        new: Dict[str, Dict[str, List[Any]]],
        *,
        price_tolerance: Optional[Number] = None,
        compact: bool = False,
) -> List[str]:
    """
    Порівнює 2-рівневі словники:
      product_name -> { position_name -> [price_str_or_num] }

    Повертає список повідомлень про різниці.
    """
    msgs: List[str] = []

    old_products = set(old.keys())
    new_products = set(new.keys())

    added_products = sorted(new_products - old_products)
    removed_products = sorted(old_products - new_products)
    common_products = sorted(old_products & new_products)

    # Додані/видалені товари
    if added_products:
        msgs.append("Додані товари:\n" + "\n".join(f"- {p}" for p in added_products))
    if removed_products:
        msgs.append("Видалені товари:\n" + "\n".join(f"- {p}" for p in removed_products))

    # Перевірка змін усередині товарів
    for product in common_products:
        old_positions = old.get(product, {})
        new_positions = new.get(product, {})

        old_pos_keys = set(old_positions.keys())
        new_pos_keys = set(new_positions.keys())

        added_pos = sorted(new_pos_keys - old_pos_keys)
        removed_pos = sorted(old_pos_keys - new_pos_keys)
        common_pos = sorted(old_pos_keys & new_pos_keys)

        product_lines: List[str] = []

            # Додані/видалені товари

        # Додані позиції
        for pos in added_pos:
            price = _parse_price(new_positions[pos])
            if compact:
                product_lines.append(f"+ {pos}")
            else:
                product_lines.append(f"- Додана позиція '{pos}': ціна {_fmt_price(price)}")

        # Видалені позиції
        for pos in removed_pos:
            price = _parse_price(old_positions[pos])
            if compact:
                product_lines.append(f"- {pos}")
            else:
                product_lines.append(f"- Видалена позиція '{pos}': була ціна {_fmt_price(price)}")

        # Зміна цін у спільних позиціях
        for pos in common_pos:
            old_price = _parse_price(old_positions[pos])
            new_price = _parse_price(new_positions[pos])

            changed = False
            if old_price is None or new_price is None:
                # якщо не можемо надійно розпарсити — порівнюємо сирі значення
                changed = (old_positions[pos] != new_positions[pos])
            else:
                if price_tolerance is None:
                    changed = (old_price != new_price)
                else:
                    changed = abs(new_price - old_price) > price_tolerance

            if changed:
                if compact:
                    product_lines.append(f"* {pos}")
                else:
                    product_lines.append(
                        f"- Зміна ціни для позиції '{pos}': "
                        f"{_fmt_price(new_price)} -> {_fmt_price(old_price)}"
                    )

        if product_lines:
            if compact:
                msgs.append(f"{product}: " + "; ".join(product_lines))
            else:
                msgs.append(f"Зміни у товарі '{product}':\n" + "\n".join(product_lines))

    if not msgs:
        msgs.append("Змін не виявлено, сьогодні смокчемо козацького прутня.")
        msgs.append(gachi())

    return msgs
