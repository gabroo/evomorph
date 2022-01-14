import { NextPage } from 'next'
import Head from 'next/head'
import Link from 'next/link'

import { Text, Container, Heading, Stack, IconButton } from '@chakra-ui/react'
import { BellIcon } from '@chakra-ui/icons'

import Jobs from '../components/Jobs'
import Models from '../components/Models'

const Header = () => (
  <Stack direction="row" align="start" justify="space-between" w="full">
    <Link href="/">
      <Heading as="button" size="xl">
        evomorph
      </Heading>
    </Link>
    <Stack direction="row" align="center">
      <Text fontSize="lg">gabroo</Text>
      <Text fontSize="sm">[logout]</Text>
    </Stack>
  </Stack>
)

const handleRun = async () => {
  const res = await fetch('https://localhost:8081/Controller/Run', {
    method: 'POST',
    cache: 'no-cache',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    },
    body: JSON.stringify({
      name: 'hello world sim',
      endMcs: 1024,
      params: {
        numCells: 256,
      },
    }),
  })
  return res
}

const runSim = async () => {
  const res = await handleRun().then(res => res.json())
  console.log(res)
}

const Run = () => (
  <Stack align="center">
    <IconButton
      aria-label="add model"
      colorScheme="red"
      rounded="lg"
      icon={<BellIcon />}
      onClick={runSim}
    />
  </Stack>
)

const Home: NextPage = () => {
  return (
    <div>
      <Head>
        <title>home &mdash; evomorph</title>
        <meta name="description" content="evomorph" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <Container maxW={'6xl'}>
        <Stack my={8} spacing={16}>
          <Header />
          <Run />
          <Models />
          <Jobs />
        </Stack>
      </Container>
    </div>
  )
}

export default Home
