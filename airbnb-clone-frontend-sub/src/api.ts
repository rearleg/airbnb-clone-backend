import { QueryFunctionContext } from "@tanstack/react-query";
import {
  CharacterDetailResponse,
  CharactersResponse,
  ComicDetailResponse,
  ComicsResponse
} from "./types";

const API_URL = "https://marvel-proxy.nomadcoders.workers.dev/v1/public";

export const listComics = (): Promise<ComicsResponse> =>
  fetch(`${API_URL}/comics`).then((r) => r.json());

export const listCharacters = (): Promise<CharactersResponse> =>
  fetch(`${API_URL}/characters`).then((r) => r.json());

export const comicDetail = ({
  queryKey
}: QueryFunctionContext): Promise<ComicDetailResponse> => {
  const [_, comicId] = queryKey;
  return fetch(`${API_URL}/comics/${comicId}`).then((r) => r.json());
};

export const characterDetail = ({
  queryKey
}: QueryFunctionContext): Promise<CharacterDetailResponse> => {
  const [_, characterId] = queryKey;
  return fetch(`${API_URL}/characters/${characterId}`).then((r) => r.json());
};

export const listComicCharacters = ({
  queryKey
}: QueryFunctionContext): Promise<CharactersResponse> => {
  const [_, comicId] = queryKey;
  return fetch(`${API_URL}/comics/${comicId}/characters`).then((r) => r.json());
};

