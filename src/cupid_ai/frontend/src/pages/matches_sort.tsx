import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select, { SelectChangeEvent } from '@mui/material/Select';

export default function MatchesSort() {
  const [sort, setSort] = React.useState("10");

  const handleChange = (event: SelectChangeEvent) => {
    setSort(event.target.value);
  };

  return (
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="sort-label">Sort</InputLabel>
      <Select
        labelId="sort-label"
        id="sort"
        value={sort}
        label="Age"
        onChange={handleChange}
      >
        <MenuItem value={10}>Urgency</MenuItem>
        <MenuItem value={20}>Distance</MenuItem>
        <MenuItem value={30}>Attractiveness</MenuItem>
      </Select>
    </FormControl>
  );
}
