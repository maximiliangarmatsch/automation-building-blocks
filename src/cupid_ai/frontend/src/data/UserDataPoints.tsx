import Languages from "./Languages.json";
import RelationshipWanteds from "./RelationshipWanteds.json";
import KidsWanteds from "./KidsWanteds.json";
import Genders from "./Genders.json";
import LivingSpaces from "./LivingSpaces.json";
import Countries from "./Countries.json";
import Smokings from "./Smokings.json";
import Drinkings from "./Drinkings.json";
import HairLengths from "./HairLengths.json";
import HairStyles from "./HairStyles.json";
import HairColors from "./HairColors.json";
import EyeColors from "./EyeColors.json";

export const UserDataPoints = [
  {
    name: "gender",
    label: "Gender",
    ui_type: "radio",
    filter_type: "radio",
    options: Genders,
  },
  {
    name: "age",
    label: "Age",
    ui_type: "input_integer",
    filter_type: "integer_minmax",
  },
  {
    name: "languages",
    label: "Languages",
    ui_type: "select_multi",
    filter_type: "select_multi",
    options: Languages,
  },
  {
    name: "distance",
    label: "Distance",
    ui_type: "",
    filter_type: "input_integer",
  },
  {
    name: "relationship_wanted",
    label: "Relationship Wanted",
    ui_type: "select_multi",
    filter_type: "select_multi",
    options: RelationshipWanteds,
  },
  {
    name: "kids_wanted",
    label: "Kids wanted",
    ui_type: "select_multi",
    filter_type: "select_multi",
    options: KidsWanteds,
  },
  {
    name: "country",
    label: "County",
    ui_type: "select",
    filter_type: "select",
    options: Countries,
  },
  {
    name: "city",
    label: "City",
    ui_type: "input_text",
    filter_type: "input_text",
  },
  {
    name: "zipcode",
    label: "Zipcode",
    ui_type: "input_text",
    filter_type: "",
  },
  {
    name: "neighborhood",
    label: "Neighborhood",
    ui_type: "input_text",
    filter_type: "",
  },
  {
    name: "occupation",
    label: "Occupation",
    ui_type: "input_text",
    filter_type: "",
  },
  {
    name: "living_space",
    label: "Living Space",
    ui_type: "select",
    filter_type: "select",
    options: LivingSpaces,
  },
  {
    name: "living_mates",
    label: "Living Mates",
    ui_type: "input_text",
    filter_type: "",
  },
  {
    name: "smoking",
    label: "Smoking",
    ui_type: "select",
    filter_type: "select",
    options: Smokings,
  },
  {
    name: "drinking",
    label: "Drinking",
    ui_type: "select",
    filter_type: "select",
    options: Drinkings,
  },

  {
    name: "attractiveness",
    label: "Attractiveness",
    ui_type: "function",
    filter_type: "float_minmax",
  },
  {
    name: "height",
    label: "Height",
    ui_type: "input_text",
    filter_type: "integer_minmax",
  },
  {
    name: "weight",
    label: "Weight",
    ui_type: "input_text",
    filter_type: "integer_minmax",
  },
  {
    name: "hair_length",
    label: "Hair Length",
    ui_type: "select",
    filter_type: "select",
    options: HairLengths,
  },
  {
    name: "hair_style",
    label: "Hair Style",
    ui_type: "select",
    filter_type: "select",
    options: HairStyles,
  },
  {
    name: "hair_color",
    label: "Hair Color",
    ui_type: "select",
    filter_type: "select",
    options: HairColors,
  },
  {
    name: "eye_color",
    label: "Eye Color",
    ui_type: "select",
    filter_type: "select",
    options: EyeColors,
  },
];
