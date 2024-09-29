using uint8_t = unsigned char;
using uint32_t = unsigned int;
using uint64_t = unsigned long long;

template <typename>
struct void_wrap { using type = void; };

namespace detail {
    template <typename T>
    struct type_identity { using type = T; };

    template <typename T>
    auto try_add_rvalue_reference(int) -> type_identity<T&&>;
    template <typename T>
    auto try_add_rvalue_reference(...) -> type_identity<T>;
}
template <typename T>
struct add_rvalue_reference : decltype(detail::try_add_rvalue_reference<T>(0)) {};

template <typename T>
typename add_rvalue_reference<T>::type declval() noexcept;

template <typename T, typename = void>
struct has_subscript {
  static constexpr bool value = false;
};
template <typename T>
struct has_subscript<T, typename void_wrap<decltype(declval<T&>()[int()])>::type> {
  static constexpr bool value = true;
};
template <typename T>
constexpr bool has_subscript_v = has_subscript<T>::value;

template <bool B, typename T = void>
struct enable_if {};
template <typename T>
struct enable_if<true, T> { typedef T type; };
template <bool B, typename T = void>
using enable_if_t = typename enable_if<B, T>::type;

template <typename, typename>
constexpr bool is_same_v = false; 
template <typename Ty>
constexpr bool is_same_v<Ty, Ty> = true;

template <typename T, T n>
struct integral_constant {
    static constexpr const T value = n;
    using type = integral_constant;
};

template <const uint8_t *S, int I = 0, const uint8_t C = S[I], typename SFINAE = enable_if_t<has_subscript_v<decltype(S)>>>
struct strlen {
    static const int value = strlen<S, I + 1, S[I+1]>::value + 1;
};
template <const uint8_t *S, int I>
struct strlen<S, I, 0> {
    static const int value = 0;
};

template <const uint8_t *S>
constexpr int strlen_v = strlen<S>::value;

template <int N>
struct factorial {
    static constexpr int value = N * factorial<N-1>::value;
};
template <>
struct factorial<1> {
    static constexpr int value = 1;
};
template <int N>
constexpr int factorial_v = factorial<N>::value;

template <bool C, typename A, typename B>
struct conditional {
    using type = B;
};
template <typename A, typename B>
struct conditional<true, A, B> {
    using type = A;
};
template <bool C, typename A, typename B>
using conditional_t = typename conditional<C, A, B>::type;

template <typename A, typename B>
struct trans {
    static constexpr const uint64_t value = A::value * 0x01919811LL + B::value;
    using type = integral_constant<uint32_t, uint32_t(value)>;
};

template <uint8_t T>
constexpr const uint8_t bin[] = "";
template <> constexpr const uint8_t bin<0>[] = "00000000";
template <> constexpr const uint8_t bin<1>[] = "00000001";
template <> constexpr const uint8_t bin<2>[] = "00000010";
template <> constexpr const uint8_t bin<3>[] = "00000011";
template <> constexpr const uint8_t bin<4>[] = "00000100";
template <> constexpr const uint8_t bin<5>[] = "00000101";
template <> constexpr const uint8_t bin<6>[] = "00000110";
template <> constexpr const uint8_t bin<7>[] = "00000111";
template <> constexpr const uint8_t bin<8>[] = "00001000";
template <> constexpr const uint8_t bin<9>[] = "00001001";
template <> constexpr const uint8_t bin<10>[] = "00001010";
template <> constexpr const uint8_t bin<11>[] = "00001011";
template <> constexpr const uint8_t bin<12>[] = "00001100";
template <> constexpr const uint8_t bin<13>[] = "00001101";
template <> constexpr const uint8_t bin<14>[] = "00001110";
template <> constexpr const uint8_t bin<15>[] = "00001111";
template <> constexpr const uint8_t bin<16>[] = "00010000";
template <> constexpr const uint8_t bin<17>[] = "00010001";
template <> constexpr const uint8_t bin<18>[] = "00010010";
template <> constexpr const uint8_t bin<19>[] = "00010011";
template <> constexpr const uint8_t bin<20>[] = "00010100";
template <> constexpr const uint8_t bin<21>[] = "00010101";
template <> constexpr const uint8_t bin<22>[] = "00010110";
template <> constexpr const uint8_t bin<23>[] = "00010111";
template <> constexpr const uint8_t bin<24>[] = "00011000";
template <> constexpr const uint8_t bin<25>[] = "00011001";
template <> constexpr const uint8_t bin<26>[] = "00011010";
template <> constexpr const uint8_t bin<27>[] = "00011011";
template <> constexpr const uint8_t bin<28>[] = "00011100";
template <> constexpr const uint8_t bin<29>[] = "00011101";
template <> constexpr const uint8_t bin<30>[] = "00011110";
template <> constexpr const uint8_t bin<31>[] = "00011111";
template <> constexpr const uint8_t bin<32>[] = "00100000";
template <> constexpr const uint8_t bin<33>[] = "00100001";
template <> constexpr const uint8_t bin<34>[] = "00100010";
template <> constexpr const uint8_t bin<35>[] = "00100011";
template <> constexpr const uint8_t bin<36>[] = "00100100";
template <> constexpr const uint8_t bin<37>[] = "00100101";
template <> constexpr const uint8_t bin<38>[] = "00100110";
template <> constexpr const uint8_t bin<39>[] = "00100111";
template <> constexpr const uint8_t bin<40>[] = "00101000";
template <> constexpr const uint8_t bin<41>[] = "00101001";
template <> constexpr const uint8_t bin<42>[] = "00101010";
template <> constexpr const uint8_t bin<43>[] = "00101011";
template <> constexpr const uint8_t bin<44>[] = "00101100";
template <> constexpr const uint8_t bin<45>[] = "00101101";
template <> constexpr const uint8_t bin<46>[] = "00101110";
template <> constexpr const uint8_t bin<47>[] = "00101111";
template <> constexpr const uint8_t bin<48>[] = "00110000";
template <> constexpr const uint8_t bin<49>[] = "00110001";
template <> constexpr const uint8_t bin<50>[] = "00110010";
template <> constexpr const uint8_t bin<51>[] = "00110011";
template <> constexpr const uint8_t bin<52>[] = "00110100";
template <> constexpr const uint8_t bin<53>[] = "00110101";
template <> constexpr const uint8_t bin<54>[] = "00110110";
template <> constexpr const uint8_t bin<55>[] = "00110111";
template <> constexpr const uint8_t bin<56>[] = "00111000";
template <> constexpr const uint8_t bin<57>[] = "00111001";
template <> constexpr const uint8_t bin<58>[] = "00111010";
template <> constexpr const uint8_t bin<59>[] = "00111011";
template <> constexpr const uint8_t bin<60>[] = "00111100";
template <> constexpr const uint8_t bin<61>[] = "00111101";
template <> constexpr const uint8_t bin<62>[] = "00111110";
template <> constexpr const uint8_t bin<63>[] = "00111111";
template <> constexpr const uint8_t bin<64>[] = "01000000";
template <> constexpr const uint8_t bin<65>[] = "01000001";
template <> constexpr const uint8_t bin<66>[] = "01000010";
template <> constexpr const uint8_t bin<67>[] = "01000011";
template <> constexpr const uint8_t bin<68>[] = "01000100";
template <> constexpr const uint8_t bin<69>[] = "01000101";
template <> constexpr const uint8_t bin<70>[] = "01000110";
template <> constexpr const uint8_t bin<71>[] = "01000111";
template <> constexpr const uint8_t bin<72>[] = "01001000";
template <> constexpr const uint8_t bin<73>[] = "01001001";
template <> constexpr const uint8_t bin<74>[] = "01001010";
template <> constexpr const uint8_t bin<75>[] = "01001011";
template <> constexpr const uint8_t bin<76>[] = "01001100";
template <> constexpr const uint8_t bin<77>[] = "01001101";
template <> constexpr const uint8_t bin<78>[] = "01001110";
template <> constexpr const uint8_t bin<79>[] = "01001111";
template <> constexpr const uint8_t bin<80>[] = "01010000";
template <> constexpr const uint8_t bin<81>[] = "01010001";
template <> constexpr const uint8_t bin<82>[] = "01010010";
template <> constexpr const uint8_t bin<83>[] = "01010011";
template <> constexpr const uint8_t bin<84>[] = "01010100";
template <> constexpr const uint8_t bin<85>[] = "01010101";
template <> constexpr const uint8_t bin<86>[] = "01010110";
template <> constexpr const uint8_t bin<87>[] = "01010111";
template <> constexpr const uint8_t bin<88>[] = "01011000";
template <> constexpr const uint8_t bin<89>[] = "01011001";
template <> constexpr const uint8_t bin<90>[] = "01011010";
template <> constexpr const uint8_t bin<91>[] = "01011011";
template <> constexpr const uint8_t bin<92>[] = "01011100";
template <> constexpr const uint8_t bin<93>[] = "01011101";
template <> constexpr const uint8_t bin<94>[] = "01011110";
template <> constexpr const uint8_t bin<95>[] = "01011111";
template <> constexpr const uint8_t bin<96>[] = "01100000";
template <> constexpr const uint8_t bin<97>[] = "01100001";
template <> constexpr const uint8_t bin<98>[] = "01100010";
template <> constexpr const uint8_t bin<99>[] = "01100011";
template <> constexpr const uint8_t bin<100>[] = "01100100";
template <> constexpr const uint8_t bin<101>[] = "01100101";
template <> constexpr const uint8_t bin<102>[] = "01100110";
template <> constexpr const uint8_t bin<103>[] = "01100111";
template <> constexpr const uint8_t bin<104>[] = "01101000";
template <> constexpr const uint8_t bin<105>[] = "01101001";
template <> constexpr const uint8_t bin<106>[] = "01101010";
template <> constexpr const uint8_t bin<107>[] = "01101011";
template <> constexpr const uint8_t bin<108>[] = "01101100";
template <> constexpr const uint8_t bin<109>[] = "01101101";
template <> constexpr const uint8_t bin<110>[] = "01101110";
template <> constexpr const uint8_t bin<111>[] = "01101111";
template <> constexpr const uint8_t bin<112>[] = "01110000";
template <> constexpr const uint8_t bin<113>[] = "01110001";
template <> constexpr const uint8_t bin<114>[] = "01110010";
template <> constexpr const uint8_t bin<115>[] = "01110011";
template <> constexpr const uint8_t bin<116>[] = "01110100";
template <> constexpr const uint8_t bin<117>[] = "01110101";
template <> constexpr const uint8_t bin<118>[] = "01110110";
template <> constexpr const uint8_t bin<119>[] = "01110111";
template <> constexpr const uint8_t bin<120>[] = "01111000";
template <> constexpr const uint8_t bin<121>[] = "01111001";
template <> constexpr const uint8_t bin<122>[] = "01111010";
template <> constexpr const uint8_t bin<123>[] = "01111011";
template <> constexpr const uint8_t bin<124>[] = "01111100";
template <> constexpr const uint8_t bin<125>[] = "01111101";
template <> constexpr const uint8_t bin<126>[] = "01111110";
template <> constexpr const uint8_t bin<127>[] = "01111111";

template <const uint8_t ...C>
struct string {
    template <const uint8_t ...T> 
    using append = string<C..., T...>;
    static constexpr const uint8_t value[] = {C...};
    static constexpr const int length = sizeof...(C);
    template <int i>
    static constexpr const uint8_t at = value[i];
};

template <typename T>
struct to_int;
template <const uint8_t a, const uint8_t b, const uint8_t c, const uint8_t d>
struct to_int<string<a, b, c, d>> {
    static constexpr const uint32_t value = a * 256 * 256 * 256LL + b * 256 * 256 + c * 256 + d;
    using type = integral_constant<uint32_t, value>;
};
template <typename T>
constexpr const uint32_t to_int_v = to_int<T>::value;

template <typename ...T>
struct group {
    static constexpr const int length = sizeof...(T);
    template <typename ...N> 
    using append = group<T..., N...>;
};

template <typename X, typename Y>
struct concat;
template <const uint8_t ...A, const uint8_t ...B>    
struct concat<string<A...>, string<B...>> {
    using type = string<A..., B...>;
};
template <typename ...A, typename ...B>    
struct concat<group<A...>, group<B...>> {
    using type = group<A..., B...>;
};
template <typename X, typename Y>
using concat_t = typename concat<X, Y>::type;

template <const uint8_t *S, int I = 0, int C = S[I]>
struct make_string {
    using type = concat_t<string<S[I]>, typename make_string<S, I+1>::type>;
};
template <const uint8_t *S, int I>
struct make_string<S, I, 0> {
    using type = string<'\0'>;
};
template <const uint8_t *S>
using make_string_t = typename make_string<S>::type;

template <typename X>
struct make_group;
template <const uint8_t c0, const uint8_t c1, const uint8_t c2, const uint8_t c3, const uint8_t ...C>
struct make_group<string<c0, c1, c2, c3, C...>> {
    using type = concat_t<group<string<c0, c1, c2, c3>>, typename make_group<string<C...>>::type>;
};
template <const uint8_t c0>
struct make_group<string<c0>> {
    using type = group<string<c0, '\0', '\0', '\0'>>;
};
template <const uint8_t c0, const uint8_t c1>
struct make_group<string<c0, c1>> {
    using type = group<string<c0, c1, '\0', '\0'>>;
};
template <const uint8_t c0, const uint8_t c1, const uint8_t c2>
struct make_group<string<c0, c1, c2>> {
    using type = group<string<c0, c1, c2, '\0'>>;
};
template <const uint8_t c0, const uint8_t c1, const uint8_t c2, const uint8_t c3>
struct make_group<string<c0, c1, c2, c3>> {
    using type = group<string<c0, c1, c2, c3>>;
};
template <typename X>
using make_group_t = typename make_group<X>::type;

template <typename T, template <typename> class F> 
struct map; 
template <template <typename> class F, typename ...L>
struct map<group<L...>, F> {
    using type = group<typename F<L>::type...>; 
};
template<typename T, template <typename> class F>
using map_t = typename map<T, F>::type;

template <typename A, typename B, template <typename, typename> class F, typename SFINAE = enable_if<A::length == B::length>> requires (A::length > 0)
struct zip;
template <template <typename, typename> class F, typename ...A, typename ...B>
struct zip<group<A...>, group<B...>, F> {
    using type = group<typename F<A, B>::type...>;
};
template <typename A, typename B, template <typename, typename> class F>
using zip_t = typename zip<A, B, F>::type;

template<uint8_t C>
concept char_printable = C >= 32 && C <= 126;

constexpr uint8_t salt[] {21, 24, 215, 9, 183, 232, 62, 241, 194, 18, 65, 50, 67, 150, 206, 250, 255, 224, 213, 19, 22, 140, 103, 11, 248, 106, 243, 5, 121, 184, 211, 77, 224, 74, 149, 228, 68, 113, 180, 26, 151, 241, 122, 177, 0};
constexpr uint8_t target[] {58, 123, 72, 156, 80, 41, 69, 186, 53, 70, 205, 115, 21, 195, 28, 247, 171, 85, 243, 183, 193, 161, 110, 209, 71, 132, 238, 189, 99, 105, 179, 193, 37, 16, 105, 37, 218, 173, 177, 193, 85, 199, 251, 254, 0};

template <const uint8_t *T>
using pack_t = map_t<make_group_t<make_string_t<T>>, to_int>;

template <const uint8_t *S, bool right = (strlen_v<S> + 1 == 14 + factorial_v<4> - 5 + strlen_v<bin<S[0]>> + 4) && is_same_v<pack_t<target>, zip_t<pack_t<S>, pack_t<salt>, trans>>, typename SFINAE = enable_if_t<right>> requires right
struct check {
    static const bool value = false;
};
template <const uint8_t *S>
struct check<S, true> {
    static const bool value = true;
};
template <const uint8_t *S>
constexpr bool check_v = check<S>::value;

template <bool C>
constexpr const uint8_t result[] = "incorrect";
template <>
constexpr uint8_t result<true>[] = "correct";

constexpr uint8_t flag[] = "-------------------------";

int main() try {
    auto ret = result<check_v<flag>>;
    if (ret[0] == 'c') {
        return 0;
    }
    return -1;
} catch (...) {
    return -2;
}
