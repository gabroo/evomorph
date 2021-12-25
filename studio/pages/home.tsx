import { NextPage } from 'next'
import Head from 'next/head'
import Link from 'next/link'

import { Text, Container, Heading, Stack } from '@chakra-ui/react'

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
          <Models />
          <Jobs />
        </Stack>
      </Container>
    </div>
  )
}

export default Home
