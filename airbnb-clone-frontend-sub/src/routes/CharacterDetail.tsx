import {
  Box,
  Button,
  Divider,
  Heading,
  HStack,
  Image,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { CharacterDetailResponse, ComicsResponse } from "../types";
import { characterDetail, comicDetail } from "../api";
import { useParams } from "react-router-dom";

export default function CharacterDetail() {
  const { characterId } = useParams();
  const { isLoading, data } = useQuery<CharacterDetailResponse>({
    queryKey: ["characters", characterId],
    queryFn: characterDetail,
  });
  const character = data?.data.results[0];
  const image = `${character?.thumbnail.path}.${character?.thumbnail.extension}`;
  return (
    <Box px={40}>
      <HStack gap={100} alignItems={"flex-start"} justifyContent="center">
        <Box rounded={"lg"} w={"400px"} h={"600px"}>
          <Image objectFit={"cover"} w={"100%"} h={"100%"} src={image} />
        </Box>
        <VStack alignItems={"flex-start"} spacing={12}>
          <Box>
            <Text color={"red"}>캐릭터 이름</Text>
            <Heading maxW={400}>{character?.name}</Heading>
            <Divider mt={8} />
          </Box>
          <Box w={400}>
            <Text color={"red"}>설명</Text>
            <Text>
              {character?.description === ""
                ? "아무것도 없습니다."
                : character?.description}
            </Text>
          </Box>

        </VStack>
      </HStack>
    </Box>
  );
}
