import { Wrap, IconButton, Stack, Heading } from '@chakra-ui/react'
import { AddIcon } from '@chakra-ui/icons'

import Form from './Form'
import Card from './Card'

import models from '../../public/models.json'
import { useState } from 'react'

const ModelList = () => (
  <Wrap spacing={4} justify='center'>
    {models.map((m, i) => (
      <Card key={i} id={m.id} name={m.name} path={m.path} desc={m.desc} />
    ))}
  </Wrap>
)
function Models() {
  const [isAdding, setIsAdding] = useState(false)
  return (
    <Stack spacing={4}>
      <Stack direction="row" justify="space-between" align="center" px={4}>
        <Heading size="lg">models</Heading>
        {!isAdding && (
          <IconButton
            aria-label="add model"
            colorScheme="blue"
            rounded="lg"
            icon={<AddIcon />}
            onClick={() => setIsAdding(true)}
          />
        )}
      </Stack>

      {isAdding ? <Form onSave={() => setIsAdding(false)} /> : <ModelList />}
    </Stack>
  )
}

export default Models
