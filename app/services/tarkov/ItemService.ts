import type { IItem } from "@/models/IItem";
import { request, gql } from "graphql-request";

export class ItemService {
  static QUERY_ALL_ITEMS = gql`
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
    const response = await request("https://api.tarkov.dev/graphql", this.QUERY_ALL_ITEMS);
    return response.items;
  }
}
