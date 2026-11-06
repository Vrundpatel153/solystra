with open('jewellery-design-html/products.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_aside = text.find('<aside')
pos_aside_end = text.find('</aside>') + len('</aside>')
pos_main = text.find('<main', pos_aside_end)
pos_main_header_end = text.find('id="products-catalog-grid"')

print("=== BETWEEN ASIDE AND GRID ===")
print(text[pos_aside_end:pos_main_header_end])

pos_last_card = text.rfind('data-product-card="true"')
pos_after_last_card = text.find('</section>', pos_last_card)
if pos_after_last_card == -1:
    pos_after_last_card = text.find('</main>', pos_last_card)

print("=== AFTER LAST CARD TO </main> ===")
print(text[pos_last_card + 50:pos_after_last_card + 100])

