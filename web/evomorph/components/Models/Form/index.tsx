import {
  Box,
  Button,
  ChakraProps,
  FormControl,
  FormLabel,
  GridItem,
  Input,
  Select,
  SimpleGrid,
  Stack,
} from '@chakra-ui/react'

interface FormProps extends ChakraProps {
  onSave: any
}

const Form = (props: FormProps) => (
  <div>
    <Stack px={4} py={5} p={[null, 6]} bg={'white'} spacing={6}>
      <SimpleGrid columns={6} spacing={6}>
        <FormControl as={GridItem} colSpan={[6, 3]}>
          <FormLabel
            htmlFor="first_name"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            First name
          </FormLabel>
          <Input
            type="text"
            name="first_name"
            id="first_name"
            autoComplete="given-name"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 3]}>
          <FormLabel
            htmlFor="last_name"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            Last name
          </FormLabel>
          <Input
            type="text"
            name="last_name"
            id="last_name"
            autoComplete="family-name"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 4]}>
          <FormLabel
            htmlFor="email_address"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            Email address
          </FormLabel>
          <Input
            type="text"
            name="email_address"
            id="email_address"
            autoComplete="email"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 3]}>
          <FormLabel
            htmlFor="country"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            Country / Region
          </FormLabel>
          <Select
            id="country"
            name="country"
            autoComplete="country"
            placeholder="Select option"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          >
            <option>United States</option>
            <option>Canada</option>
            <option>Mexico</option>
          </Select>
        </FormControl>

        <FormControl as={GridItem} colSpan={6}>
          <FormLabel
            htmlFor="street_address"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            Street address
          </FormLabel>
          <Input
            type="text"
            name="street_address"
            id="street_address"
            autoComplete="street-address"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 6, null, 2]}>
          <FormLabel
            htmlFor="city"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            City
          </FormLabel>
          <Input
            type="text"
            name="city"
            id="city"
            autoComplete="city"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 3, null, 2]}>
          <FormLabel
            htmlFor="state"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            State / Province
          </FormLabel>
          <Input
            type="text"
            name="state"
            id="state"
            autoComplete="state"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>

        <FormControl as={GridItem} colSpan={[6, 3, null, 2]}>
          <FormLabel
            htmlFor="postal_code"
            fontSize="sm"
            fontWeight="md"
            color={'gray.700'}
          >
            ZIP / Postal
          </FormLabel>
          <Input
            type="text"
            name="postal_code"
            id="postal_code"
            autoComplete="postal-code"
            mt={1}
            focusBorderColor="brand.400"
            shadow="sm"
            size="sm"
            w="full"
            rounded="md"
          />
        </FormControl>
      </SimpleGrid>
    </Stack>
    <Box px={{ base: 4, sm: 6 }} py={3} textAlign="right">
      <Button onClick={props.onSave} colorScheme="blue" fontWeight="md">
        Save
      </Button>
    </Box>
  </div>
)

export default Form
