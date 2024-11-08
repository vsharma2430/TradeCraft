from jugaad_data.nse import NSELive

n = NSELive()
q = n.stock_quote("HDFC")
print(q)
