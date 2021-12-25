import { NextPage } from 'next'
import Head from 'next/head'
import { Stack, Heading, Text, Button, Container } from '@chakra-ui/react'
import Link from 'next/link'

const Index: NextPage = () => {
  return (
    <div>
      <Head>
        <title>evomorph</title>
        <meta name="description" content="evomorph" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container maxW={'5xl'}>
        <Stack spacing={{ base: 8, md: 10 }} py={{ base: 20, md: 28 }}>
          <Heading
            fontWeight={600}
            fontSize={{ base: '3xl', sm: '4xl', md: '6xl' }}
            lineHeight={'110%'}
          >
            evomorph
          </Heading>
          <Text color={'gray.500'} maxW={'3xl'}>
            Some text about evomorph. I don't know what to put on the home page.
          </Text>
          <Text color={'gray.500'} maxW={'3xl'}>
            "Now, I <i>only</i> use evomorph." &nbsp;&nbsp;
            <b>&mdash;Reviewer #2</b>
          </Text>
          <Stack spacing={6} direction={'row'}>
            <Link href="/home">
              <Button rounded="full" px={6} colorScheme={'blue'}>
                enter&nbsp;&nbsp;&rarr;
              </Button>
            </Link>
          </Stack>
        </Stack>
      </Container>
    </div>
  )
}

export default Index
