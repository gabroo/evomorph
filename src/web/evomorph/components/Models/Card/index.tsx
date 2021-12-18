import { Stack, ChakraProps, Flex, Text, Icon, Heading } from '@chakra-ui/react'
import { GoFileCode, GoTag } from 'react-icons/go'

interface CardProps extends ChakraProps {
  id: string
  name: string
  path: string
  desc: string
}

const Card = (props: CardProps) => {
  return (
    <Stack
      w='2xs'
      h='xs'
      mx='auto'
      borderWidth="2px"
      borderColor="gray.200"
      rounded="lg"
      p={8}
      justifyContent="space-between"
    >
      <div>
        <Heading size="md">{props.name}</Heading>

        <Text fontSize="sm" py={2}>
          {props.desc}
        </Text>
      </div>

      <div>
        <Flex alignItems="center" mt={4}>
          <Icon as={GoFileCode} />
          <Text px={2} fontSize="xs" fontFamily="monospace" fontWeight="bold">
            {props.path}
          </Text>
        </Flex>
        <Flex alignItems="center" mt={4}>
          <Icon as={GoTag} />
          <Text px={2} fontSize="xs" fontFamily="monospace" fontWeight="bold">
            {props.id}
          </Text>
        </Flex>
      </div>
    </Stack >
  )
}

export default Card
