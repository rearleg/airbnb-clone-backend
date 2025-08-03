import { Button, Divider, HStack, Image, Text, VStack } from "@chakra-ui/react";

export default function Header() {
  return (
    <VStack m={8} justifyContent={"center"}>
      <Image
        height={"50px"}
        src="https://upload.wikimedia.org/wikipedia/commons/b/b9/Marvel_Logo.svg"
      />
      <HStack spacing={20} mt={8}>
        <Button
          as={"a"}
          href="/"
          _hover={{
            color: "red",
            textDecoration: "underline",
          }}
          fontSize={"md"}
          variant={"link"}
        >
          코믹스 리스트
        </Button>
        <Button
          as={"a"}
          href="/characters"
          _hover={{
            color: "red",
            textDecoration: "underline",
          }}
          fontSize={"md"}
          variant={"link"}
        >
          캐릭터 리스트
        </Button>
      </HStack>
      <Divider borderColor={"gray"} />
    </VStack>
  );
}
