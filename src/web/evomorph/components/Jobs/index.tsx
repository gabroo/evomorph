import { useState } from "react"

import { AddIcon, ArrowBackIcon, ArrowForwardIcon } from '@chakra-ui/icons'
import { Heading, IconButton, Stack, Text } from '@chakra-ui/react'

import Job from './Job'

import sims from '../../public/sims.json'

function Jobs() {
  const [page, setPage] = useState(0)
  const JOBS_PER_PAGE = 4
  const END_PAGE = Math.ceil(sims.length / JOBS_PER_PAGE)
  const jobs = sims.slice(page * JOBS_PER_PAGE, (page + 1) * JOBS_PER_PAGE)
  return (
    <Stack spacing={4}>
      <Stack direction="row" justify="space-between" align="center" px={4}>
        <Heading size="lg">jobs</Heading>
        <IconButton
          aria-label="add job"
          colorScheme="blue"
          rounded="lg"
          icon={<AddIcon />} />
      </Stack>
      <Stack direction="column" align="center" w="full" spacing={4}>
        {jobs.map((sim, i) => (
          <Job
            key={i}
            id={sim.id}
            name={sim.name}
            model={sim.model}
            params={sim.params} />
        ))}
      </Stack>
      <Stack direction="row" justify="end" align="center" spacing={4}>
        <IconButton
          aria-label="previous page"
          rounded="lg"
          icon={<ArrowBackIcon />}
          disabled={page == 0}
          onClick={() => setPage((page) => page - 1)} />
        <Text>
          {page + 1} of {END_PAGE}
        </Text>
        <IconButton
          aria-label="next page"
          rounded="lg"
          icon={<ArrowForwardIcon />}
          disabled={page == END_PAGE - 1}
          onClick={() => setPage((page) => page + 1)} />
      </Stack>
    </Stack>
  )
}

export default Jobs
