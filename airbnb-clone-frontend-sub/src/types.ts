export interface Thumbnail {
  path: string;
  extension: string;
}

export interface Item {
  resourceURI: string;
  name: string;
}

export interface Comics {
  available: number;
  collectionURI: string;
  items: Item[];
  returned: number;
}

export interface Item2 {
  resourceURI: string;
  name: string;
}

export interface Series {
  available: number;
  collectionURI: string;
  items: Item2[];
  returned: number;
}

export interface Item3 {
  resourceURI: string;
  name: string;
  type: string;
}

export interface Stories {
  available: number;
  collectionURI: string;
  items: Item3[];
  returned: number;
}

export interface Item4 {
  resourceURI: string;
  name: string;
}

export interface Events {
  available: number;
  collectionURI: string;
  items: Item4[];
  returned: number;
}

export interface Url {
  type: string;
  url: string;
}

export interface CharactersResult {
  id: number;
  name: string;
  description: string;
  modified: Date;
  thumbnail: Thumbnail;
  resourceURI: string;
  comics: Comics;
  series: Series;
  stories: Stories;
  events: Events;
  urls: Url[];
}

export interface CharactersData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: CharactersResult[];
}

export interface CharactersResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: CharactersData;
}

export interface TextObject {
  type: string;
  language: string;
  text: string;
}

export interface Variant {
  resourceURI: string;
  name: string;
}

export interface CollectedIssue {
  resourceURI: string;
  name: string;
}

export interface Date {
  type: string;
  date: any;
}

export interface Price {
  type: string;
  price: number;
}

export interface Image {
  path: string;
  extension: string;
}

export interface Creators {
  available: number;
  collectionURI: string;
  items: Item[];
  returned: number;
}

export interface Characters {
  available: number;
  collectionURI: string;
  items: Item2[];
  returned: number;
}

export interface ComicsResult {
  id: number;
  digitalId: number;
  title: string; //
  issueNumber: number;
  variantDescription: string;
  description: string;
  modified: any;
  isbn: string;
  upc: string;
  diamondCode: string;
  ean: string;
  issn: string;
  format: string;
  pageCount: number;
  textObjects: TextObject[];
  resourceURI: string;
  urls: Url[];
  series: Series; //
  variants: Variant[];
  collections: any[];
  collectedIssues: CollectedIssue[];
  dates: Date[];
  prices: Price[];
  thumbnail: Thumbnail; //
  images: Image[];
  creators: Creators;
  characters: Characters;
  stories: Stories;
  events: Events;
}

export interface ComicsData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: ComicsResult[];
}

export interface ComicsResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: ComicsData;
}

export interface Item5 {
  resourceURI: string;
  name: string;
}

export interface Next {
  resourceURI: string;
  name: string;
}

export interface Previous {
  resourceURI: string;
  name: string;
}

export interface EventsResult {
  id: number;
  title: string;
  description: string;
  resourceURI: string;
  urls: Url[];
  modified: Date;
  start: string;
  end: string;
  thumbnail: Thumbnail;
  creators: Creators;
  characters: Characters;
  stories: Stories;
  comics: Comics;
  series: Series;
  next: Next;
  previous: Previous;
}

export interface EventsData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: EventsResult[];
}

export interface EventsResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: EventsData;
}

export interface Collection {
  resourceURI: string;
  name: string;
}

export interface ComicDetailResult {
  id: number;
  digitalId: number;
  title: string;
  issueNumber: number;
  variantDescription: string;
  description: string;
  modified: Date;
  isbn: string;
  upc: string;
  diamondCode: string;
  ean: string;
  issn: string;
  format: string;
  pageCount: number;
  textObjects: TextObject[];
  resourceURI: string;
  urls: Url[];
  series: Series;
  variants: any[];
  collections: Collection[];
  collectedIssues: any[];
  dates: Date[];
  prices: Price[];
  thumbnail: Thumbnail;
  images: Image[];
  creators: Creators;
  characters: Characters;
  stories: Stories;
  events: Events;
}

export interface ComicDetailData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: ComicDetailResult[];
}

export interface ComicDetailResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: ComicDetailData;
}

export interface CharacterDetailResult {
  id: number;
  name: string;
  description: string;
  modified: Date;
  thumbnail: Thumbnail;
  resourceURI: string;
  comics: Comics;
  series: Series;
  stories: Stories;
  events: Events;
  urls: Url[];
}

export interface CharacterDetailData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: CharacterDetailResult[];
}

export interface CharacterDetailResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: CharacterDetailData;
}

export interface EventDetailResult {
  id: number;
  title: string;
  description: string;
  resourceURI: string;
  urls: Url[];
  modified: Date;
  start?: any;
  end?: any;
  thumbnail: Thumbnail;
  creators: Creators;
  characters: Characters;
  stories: Stories;
  comics: Comics;
  series: Series;
  next?: any;
  previous?: any;
}

export interface EventDetailData {
  offset: number;
  limit: number;
  total: number;
  count: number;
  results: EventDetailResult[];
}

export interface EventDetailResponse {
  code: number;
  status: string;
  copyright: string;
  attributionText: string;
  attributionHTML: string;
  etag: string;
  data: EventDetailData;
}
