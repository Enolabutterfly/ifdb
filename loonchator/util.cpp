#define UNICODE
#include <windows.h>


#include "util.h"

std::wstring Conv(const std::string& str) {
  if (str.empty()) return {};
  std::vector<wchar_t> buf(str.size());
  auto sz = MultiByteToWideChar(CP_UTF8, 0, str.data(), str.size(), &buf[0],
                                buf.size());
  return {buf.begin(), buf.begin() + sz};
}

std::string Conv(const std::wstring& str) {
  if (str.empty()) return {};
  std::vector<char> buf(str.size() * 4);
  auto sz = WideCharToMultiByte(CP_UTF8, 0, str.data(), str.size(), &buf[0],
                                buf.size(), 0, nullptr);
  return {buf.begin(), buf.begin() + sz};
}
