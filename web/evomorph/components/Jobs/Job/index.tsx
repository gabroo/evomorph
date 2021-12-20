import { ChevronRightIcon, EditIcon } from '@chakra-ui/icons'
import {
  Badge,
  ChakraProps,
  Spinner,
  IconButton,
  Stack,
  Text,
} from '@chakra-ui/react'
import { useState } from 'react'

type Parameter = {
  name: string
  value: number
}

interface JobProps extends ChakraProps {
  id: string
  name: string
  model: string
  params: Parameter[]
}

const Job = (props: JobProps) => {
  const [running, setRunning] = useState(false)
  return (
    <Stack
      direction="row"
      justify="space-between"
      align="center"
      w="full"
      p={5}
      borderWidth="2px"
      borderColor="gray.200"
      rounded="lg"
    >
      <Text flex={2} noOfLines={1}>
        {props.name}
      </Text>
      <Text flex={3} noOfLines={1}>
        <Badge>model</Badge>
        &nbsp;&nbsp;
        {props.model}
      </Text>
      <Stack direction="row" justify="end" spacing={4} flex={1}>
        <IconButton
          aria-label="edit job"
          rounded="lg"
          colorScheme="blackAlpha"
          icon={<EditIcon />}
        />
        <IconButton
          aria-label="run job"
          rounded="lg"
          colorScheme={running ? "orange" : "green"}
          icon={
            running ? <Spinner /> : <ChevronRightIcon boxSize='2rem' />
          }
          onClick={() => setRunning((r) => !r)}
        />
      </Stack>
    </Stack>
  )
}

export default Job
