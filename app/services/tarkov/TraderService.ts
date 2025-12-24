import type { ITrader } from "@/models/ITrader";
import { request, gql } from "graphql-request";

export class TraderService {
  static QUERY_ALL_TRADERS = gql`
    query {
      traders {
        name
        normalizedName
        imageLink
        image4xLink
        currency {
          name
          normalizedName
          shortName
        }
      }
    }
  `;
  public static async getAllTraders(): Promise<ITrader[]> {
    const response = await request("https://api.tarkov.dev/graphql", this.QUERY_ALL_TRADERS);
    return response.traders;
  }
}
