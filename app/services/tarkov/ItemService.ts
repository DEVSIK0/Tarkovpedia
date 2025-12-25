import type { IItem } from "@/models/IItem";
import { request, gql } from "graphql-request";

export class ItemService {
  private static readonly API_URL = "https://api.tarkov.dev/graphql";

  private static readonly QUERY_ALL_ITEMS = gql`
    query {
      items {
        avg24hPrice
        basePrice
        description
        height
        id
        image8xLink
        inspectImageLink
        gridImageLink
        link
        name
        normalizedName
        shortName
        weight
        wikiLink
        minLevelForFlea
        sellFor {
          price
          currency
          priceRUB
          vendor {
            name
            normalizedName
          }
        }
      }
    }
  `;

  public static async getAllItems(): Promise<IItem[]> {
    try {
      const response = await request<{ items: IItem[] }>(this.API_URL, this.QUERY_ALL_ITEMS);
      return this.processItems(response.items);
    } catch (error) {
      console.error("Failed to fetch items:", error);
      throw error;
    }
  }

  private static processItems(items: IItem[]): IItem[] {
    return items.map((item) => {
      item.sellFor = item.sellFor
        .filter((sell) => sell.vendor.normalizedName !== "ref")
        .sort((a, b) => b.priceRUB - a.priceRUB);
      return item;
    });
  }
}
