from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, uvicorn

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/{barcode}")
async def nutritions(barcode: str = "6281018154549"):
    nutritions: list[dict[str, str]] = []
    item_index = 0
    with open("./products.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i, item in enumerate(data.get("products", [])):
            if barcode in item.get("attributes", {}).get("barCodes", []):
                nutritions = item.get("classificationAttributes", {})[
                    0].get("features", [])
                item_index = i
    product = {
        "data": {}
    }
    for i, item in enumerate(nutritions):
        product['data'] |= {
            item.get("code"): item.get(list(item.keys())[0])
        }
    product['data']['name_ar'] = data['products'][item_index].get(
        "attributes", {}).get('name_ar', "")
    product['data']['name_en'] = data['products'][item_index].get(
        'name_en', "")

    return product

@app.get("/media/{barcode}")
async def get_product_media(barcode: str = "6281018154549"):

    with open("./products.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        for i, item in enumerate(data.get("products", [])):
            if barcode in item.get("attributes", {}).get("barCodes", []):
                    return item.get("media")
    return 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="192.168.1.2", port=5000)