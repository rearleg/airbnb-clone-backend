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
import { ComicsResponse } from "../types";
import { comicDetail } from "../api";
import { useParams } from "react-router-dom";

export default function ComicDetail() {
  const { comicId } = useParams();
  const { isLoading, data } = useQuery<ComicsResponse>({
    queryKey: ["comics", comicId],
    queryFn: comicDetail,
  });
  const comic = data?.data.results[0];
  const image = `${comic?.thumbnail.path}.${comic?.thumbnail.extension}`;
  return (
    <Box px={40}>
      <HStack gap={100} alignItems={"flex-start"} justifyContent="center">
        <Box rounded={"lg"} w={"400px"} h={"600px"}>
          <Image objectFit={"cover"} w={"100%"} h={"100%"} src={image} />
        </Box>
        <VStack alignItems={"flex-start"} spacing={12}>
          <Box>
            <Text color={"red"}>코믹스 제목</Text>
            <Heading maxW={400}>{comic?.title}</Heading>
            <Divider mt={8} />
          </Box>
          <Box w={400}>
            <Text color={"red"}>설명</Text>
            <Text>
              {comic?.description === ""
                ? "아무것도 없습니다."
                : comic?.description}
            </Text>
          </Box>
          <Button as={"a"} href={`/comics/${comicId}/characters`} colorScheme="red" color={"white"}>
            등장 캐릭터 보기
          </Button>
        </VStack>
      </HStack>
    </Box>
  );
}
